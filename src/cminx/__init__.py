# Copyright 2021 CMakePP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""
Generate Sphinx-compatible RST documentation for CMake files.
Documentation is written in a special form of block comments,
denoted by the starting characters :code: `#[[[` and ending with the standard :code: `#]]`.

:Author: Branden Butler
:License: Apache 2.0
"""

import argparse
import copy
import logging
import logging.config
import os
import re
import sys
import logging.config
from typing import List

import pathspec
from confuse import Configuration
from pkg_resources import get_distribution, DistributionNotFound

from .config import config_template, dict_to_settings, Settings
from .documenter import Documenter
from .rstwriter import RSTWriter

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    __version__ = "UNKNOWN"

logger: logging.Logger = logging.getLogger(__name__)


def main(args: List[str] = tuple(sys.argv[1:])):
    """
    CMake Documentation Generator program entry point.

    :param args: Array of strings containing program arguments, excluding program name. Same format as sys.argv[1:].
    """

    global logger

    parser = argparse.ArgumentParser(
        description="Automatic documentation generator for CMake files. This program " +
                    "generates Sphinx-compatible RST documents, which are incompatible "
                    "with standard docutils. Config files are searched for according to "
                    "operating-system-dependent directories, such as "
                    "$XDG_CONFIG_HOME/cminx on Linux. Additional config files can be "
                    "specified with the -s option.")
    parser.add_argument(
        "files",
        nargs="+",
        help="CMake file to generate documentation for. If directory, will generate documentation for "
             "all *.cmake files (case-insensitive)")
    parser.add_argument(
        "-o",
        "--output",
        help="Directory to output generated RST to. If not specified will print to standard output. "
             "Output files will have the original filename with the cmake extension replaced by .rst",
        dest="output.directory")
    parser.add_argument(
        "-r",
        "--recursive",
        help="If specified, will generate documentation for all subdirectories of specified directory "
             "recursively. If the prefix is not specified, it will be set to the last element of the "
             "input path.",
        action="store_true",
        default=None,
        dest="input.recursive")
    parser.add_argument(
        "-p",
        "--prefix",
        help="If specified, all output files will have headers generated as if the prefix was the top "
             "level package.",
        dest="rst.prefix")
    parser.add_argument(
        "-s",
        "--settings",
        help="Load settings from the specified YAML file. Parameters specified by "
             "this file will override defaults, and command-line arguments will "
             "override both.")
    parser.add_argument(
        "-e",
        "--exclude",
        help="Exclude some files from documentation. Supports shell-style glob syntax, relative paths "
        "are resolved with respect to the current working directory.",
        dest="input.exclude_filters",
        action="append")
    parser.add_argument(
        "--version",
        action='version',
        version='%(prog)s version ' +
                __version__)

    args = parser.parse_args(args)
    settings = Configuration("cminx", __name__)

    if args.settings is not None:
        # Additional settings file was defined on the command line
        settings.set_file(os.path.abspath(args.settings))

    settings.set_args(args, dots=True)

    output_dir_relative_to_config = False

    if settings["output"]["relative_to_config"].get():
        output_dir_relative_to_config = True

    settings_dict = settings.get(
        config_template(output_dir_relative_to_config))

    settings_obj = dict_to_settings(settings_dict)

    # Concatenate all exclude filters rather than overriding the entire list
    settings_obj.input.exclude_filters = list(
        settings["input"]["exclude_filters"].all_contents())

    # Load Python logging configuration from settings
    logging.config.dictConfig(settings_obj.logging.logger_config)
    logger = logging.getLogger(__name__)

    logger.debug(f"Exclude filters: {settings_obj.input.exclude_filters}")

    if settings_dict["output"]["directory"] is not None:
        output_path = os.path.abspath(settings_dict["output"]["directory"])
        logger.info(f"Writing RST files to {output_path}")

    for input_file in args.files:
        # Process all files specified on command line
        document(input_file, settings_obj)


def document(input_file: str, settings: Settings):
    """
    Handler for documenting CMake files or all files in a directory. Performs
    preprocessing before handing off to document_single_file over all detected
    files. Also generates index.rst files for all directories.

    :param input_file: String locating a file or directory to document.
    :param settings: Object containing all necessary settings that will be passed down to the
    documenter, aggregator, and RST writer.
    """
    output_path: str = settings.output.directory
    recursive = settings.input.recursive
    prefix = settings.rst.prefix

    # We copy because we're going to modify the
    # settings to pass down to lower layers during
    # preprocessing
    new_settings = copy.deepcopy(settings)

    input_path = os.path.abspath(input_file)
    if os.path.isdir(input_path):
        # os.path.join() adds a trailing slash to directories if absent
        input_path = os.path.join(input_path, '')

    spec = pathspec.PathSpec.from_lines(
        pathspec.patterns.GitWildMatchPattern,
        settings.input.exclude_filters)

    logger.debug(f"Input path: {input_path}")

    # If the input path matches the exclusion pattern, then ignore
    # this whole path
    if spec.match_file(input_path):
        return

    if not os.path.exists(input_path):
        logger.error(f"File or directory \"{input_path}\" does not exist")
        exit(-1)
    elif os.path.isfile(input_path):
        # If the input was a regular file,
        # don't do anything special and just document the single file
        if output_path is not None:
            os.makedirs(output_path, exist_ok=True)
        document_single_file(input_path, input_path, new_settings)
    elif os.path.isdir(input_path):
        # Input was a directory, so we need to do a lot of preprocessing

        last_dir_element = os.path.basename(os.path.normpath(input_file))
        prefix = prefix if prefix is not None else last_dir_element
        new_settings.rst.prefix = prefix

        # Walk dir and add cmake files to list
        for root, subdirs, filenames in os.walk(
                input_path, topdown=True, followlinks=settings.input.follow_symlinks):

            logger.debug(f"Subdirs: {subdirs}")
            logger.debug(f"Root: {root}")

            # Check our subdirs and see if any match the exclusion filters
            # If they do, remove from the list and os.walk() will ignore them
            for subdir in subdirs:
                # The extra os.path.join() with an empty string ensures the
                # directory has a trailing slash
                if spec.match_file(
                    os.path.join(
                        root,
                        os.path.join(
                            subdir,
                            ""))):
                    subdirs.remove(subdir)

            # Check if any files match the exclusion filters
            # If they do, remove them and the rest of the processing
            # will ignore them
            for file in filenames:
                if spec.match_file(os.path.join(root, file)):
                    filenames.remove(file)

            # Check subdirs and files to make sure .cmake files
            # are present, if not then ignore
            if settings.input.auto_exclude_directories_without_cmake:
                # Make a copy because modifying while iterating results in
                # skipping some entries
                for subdir in copy.copy(subdirs):
                    logger.debug(f"Checking filenames in subdir {subdir}")
                    for filename in os.scandir(os.path.join(root, subdir)):
                        if filename.is_file() and filename.path.endswith(".cmake"):
                            break
                    # If we exited loop normally, i.e. a .cmake file was not
                    # found
                    else:
                        subdirs.remove(subdir)

                # Check if files in current dir contain .cmake
                # If not, ignore this dir and continue walking
                for filename in filenames:
                    if filename.endswith(".cmake"):
                        break
                else:
                    continue

            # Sort filenames and subdirs in alphabetical order
            filenames = sorted(filenames)
            subdirs = sorted(subdirs)

            # If we want to output to an actual file
            # and not stdout
            if output_path is not None:
                path = os.path.join(
                    output_path, os.path.relpath(
                        root, input_path))
                # Make sure we have all the directories created
                os.makedirs(path, exist_ok=True)

                rel_path = os.path.relpath(root, input_path)

                # We need to create an index.rst file for each directory
                index = RSTWriter(rel_path, settings=settings)

                if prefix is not None:
                    # If current file dir is same as root dir, replace "." with
                    # prefix
                    if index.title == settings.rst.module_path_separator:
                        index.title = prefix
                    else:
                        # Add prefix to beginning of header
                        index.title = prefix + settings.rst.module_path_separator + index.title

                toctree = index.directive("toctree")
                toctree.option("maxdepth", 2)

                if recursive:
                    for directory in subdirs:
                        toctree.text(os.path.join(directory, "index.rst"))

                # Filter filenames for cmake files, then add a toctree entry
                for file in [f for f in filenames if f.lower().endswith(".cmake")]:
                    toctree.text('.'.join(file.split('.')[:-1]))


                index.write_to_file(
                    os.path.join(
                        os.path.join(
                            output_path,
                            rel_path),
                        "index.rst"))

            # All preprocessing is complete and we have
            # our index.rst, now just loop over files with the .cmake
            # extension and document them
            for file in filenames:
                if "cmake" == file.split(".")[-1].lower():
                    document_single_file(
                        os.path.join(
                            root,
                            file),
                        input_path,
                        new_settings)

            if not recursive:
                break

    else:
        logger.error("File is a special file (socket, FIFO, device file) and is unsupported")


def document_single_file(file, root, settings: Settings):
    """
    Documents a single file, generates the RST, and places the file in the respective directory if output_dir
    specified.

    :param file: Path to the CMake file to be documented
    :param root: Directory considered to be the root of the source tree. The RST header and output tree will be
    generated from the relative path between file and root
    :param settings: Object containing all necessary settings that will be passed down to the
    documenter, aggregator, and RST writer.
    """

    output_path: str = settings.output.directory
    prefix = settings.rst.prefix
    module_path_separator = settings.rst.module_path_separator

    if os.path.isdir(root):
        # Path to file relative to input_path
        header_name = os.path.relpath(file, root)
    else:
        header_name = file

    if prefix is not None:
        # If current file dir is same as root dir, replace "." with prefix
        if header_name == module_path_separator:
            header_name = prefix
        else:
            # Add prefix to beginning of headers
            header_name = prefix + module_path_separator + header_name

    module_name = header_name

    # Clean header and module names if desired
    # by removing extension

    if not settings.rst.file_extensions_in_titles:
        header_name = re.sub(r"\.cmake$", "", header_name)

    if not settings.rst.file_extensions_in_modules:
        module_name = re.sub(r"\.cmake$", "", module_name)

    # Only log when not writing to stdout
    if output_path is not None:
        logger.info(f"Writing for file {file}")

    auto_documenter = Documenter(file, header_name, module_name, settings)

    output_writer = auto_documenter.process()
    if output_path is not None:
        # Determine where to place generated RST file
        os.makedirs(output_path, exist_ok=True)
        if os.path.isdir(output_path):
            output_filename = os.path.join(
                output_path, ".".join(
                    os.path.basename(file).split(".")[
                    :-1]) + ".rst")
            if os.path.isdir(root):
                # Path to file relative to input_path
                subpath = os.path.relpath(file, root)
                output_filename = os.path.join(
                    output_path, os.path.join(
                        os.path.dirname(subpath), ".".join(
                            os.path.basename(file).split(".")[
                            :-1]) + ".rst"))
            logger.info(f"Writing RST file {output_filename}")
            output_writer.write_to_file(output_filename)
    else:  # Output was not specified so print to screen
        # Use print() for raw output instead of logger
        print(str(output_writer) + "\n")
