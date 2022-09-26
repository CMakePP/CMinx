.. Copyright 2021 CMakePP
..
.. Licensed under the Apache License, Version 2.0 (the "License");
.. you may not use this file except in compliance with the License.
.. You may obtain a copy of the License at
..
.. http://www.apache.org/licenses/LICENSE-2.0
..
.. Unless required by applicable law or agreed to in writing, software
.. distributed under the License is distributed on an "AS IS" BASIS,
.. WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
.. See the License for the specific language governing permissions and
.. limitations under the License.
..
#####
Usage
#####

For each CMake function or variable that you would like to document, prepend it
with a block doc-comment. A block doc-comment begins with :code:`#[[[` and ends
with :code:`#]]`.

Then run :code:`cminx` on your CMake files, outputting to a directory of your
choosing. The help text is printed below for reference::

   usage: cminx [-h] [-o OUTPUT.DIRECTORY] [-r] [-p RST.PREFIX] [-s SETTINGS]
                [-e INPUT.EXCLUDE_FILTERS] [--version]
                files [files ...]

   Automatic documentation generator for CMake files. This program generates
   Sphinx-compatible RST documents, which are incompatible with standard
   docutils. Config files are searched for according to operating-system-
   dependent directories, such as $XDG_CONFIG_HOME/cminx on Linux. Additional
   config files can be specified with the -s option.

   positional arguments:
      files             CMake file to generate documentation for. If
                        directory, will generate documentation for all *.cmake
                        files (case-insensitive)

   options:
      -h, --help            show this help message and exit
      -o OUTPUT.DIRECTORY, --output OUTPUT.DIRECTORY
                            Directory to output generated RST to. If not specified
                            will print to standard output. Output files will have
                            the original filename with the cmake extension
                            replaced by .rst
      -r, --recursive       If specified, will generate documentation for all
                            subdirectories of specified directory recursively. If
                            the prefix is not specified, it will be set to the
                            last element of the input path.
      -p RST.PREFIX, --prefix RST.PREFIX
                            If specified, all output files will have headers
                            generated as if the prefix was the top level package.
      -s SETTINGS, --settings SETTINGS
                           Load settings from the specified YAML file. Parameters
                           specified by this file will override defaults, and
                           command-line arguments will override both.
      -e INPUT.EXCLUDE_FILTERS, --exclude INPUT.EXCLUDE_FILTERS
                           Exclude some files from documentation. Supports shell-
                           style glob syntax, relative paths are resolved with
                           respect to the current working directory.
      --version            show program's version number and exit
