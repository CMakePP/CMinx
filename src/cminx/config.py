# Copyright 2022 CMakePP
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

import confuse
import os
from typing import List
from dataclasses import dataclass, field


def config_template(output_dir_relative_to_config: bool = False) -> dict:
    """
    Generates the config template.

    :param output_dir_relative_to_config: Selects whether output.dir should be resolved relative to the config source,
    if not then it is resolved relative to the current working directory.
    """
    return {
        "input": {
            "include_undocumented_function": bool,
            "include_undocumented_macro": bool,
            "include_undocumented_cpp_class": bool,
            "include_undocumented_cpp_attr": bool,
            "include_undocumented_cpp_constructor": bool,
            "include_undocumented_cpp_member": bool,
            "include_undocumented_ct_add_test": bool,
            "include_undocumented_add_test": bool,
            "include_undocumented_ct_add_section": bool,
            "include_undocumented_option": bool,
            "auto_exclude_directories_without_cmake": bool,
            "kwargs_doc_trigger_string": confuse.Optional(confuse.String(), default=":keyword"),
            "exclude_filters": confuse.Optional(list, default=()),
            "recursive": bool,
            "follow_symlinks": bool
        },
        "output": {
            "directory": confuse.Optional(
                confuse.Filename(cwd=os.getcwd()) if not output_dir_relative_to_config
                else confuse.Filename(in_source_dir=True)),
            "relative_to_config": bool
        },
        "logging": confuse.TypeTemplate(dict),
        "rst": {
            "file_extensions_in_titles": bool,
            "file_extensions_in_modules": bool,
            "module_path_separator": ".",
            "headers": confuse.StrSeq(),
            "prefix": confuse.Optional(confuse.String())
        }

    }


@dataclass
class InputSettings:
    include_undocumented_function: bool = True
    include_undocumented_macro: bool = True
    include_undocumented_cpp_class: bool = True
    include_undocumented_cpp_attr: bool = True
    include_undocumented_cpp_constructor: bool = True
    include_undocumented_cpp_member: bool = True
    include_undocumented_ct_add_test: bool = True
    include_undocumented_ct_add_section: bool = True
    include_undocumented_add_test: bool = True
    include_undocumented_option: bool = True
    auto_exclude_directories_without_cmake: bool = True
    kwargs_doc_trigger_string: str = ":param **kwargs:"
    exclude_filters: List[str] = ()
    recursive: bool = False
    follow_symlinks: bool = False


@dataclass
class OutputSettings:
    directory: str = None
    relative_to_config: bool = False


@dataclass
class LoggingSettings:
    logger_config: dict = field(default_factory=lambda: ({}))


@dataclass
class RSTSettings:
    file_extensions_in_titles: bool = False
    file_extensions_in_modules: bool = False
    prefix: str = None
    module_path_separator: str = "."
    headers: List[str] = ('#', '*', '=', '-', '_', '~', '!', '&', '@', '^')


@dataclass
class Settings:
    input: InputSettings = field(default_factory=lambda: InputSettings())
    output: OutputSettings = field(default_factory=lambda: OutputSettings())
    logging: LoggingSettings = field(default_factory=lambda: LoggingSettings())
    rst: RSTSettings = field(default_factory=lambda: RSTSettings())


def dict_to_settings(input_dict: dict) -> Settings:
    input_settings = InputSettings(**input_dict["input"])
    output_settings = OutputSettings(**input_dict["output"])
    logging_settings = LoggingSettings(input_dict["logging"])
    rst_settings = RSTSettings(**input_dict["rst"])
    return Settings(
        input_settings,
        output_settings,
        logging_settings,
        rst_settings)
