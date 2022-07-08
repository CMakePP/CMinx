import confuse
import os
from typing import List
from dataclasses import dataclass


def config_template(output_dir_relative_to_config=False):
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
            "include_undocumented_cpp_member": bool,
            "include_undocumented_ct_add_test": bool,
            "include_undocumented_ct_add_section": bool,
            "recursive": bool
        },
        "output": {
            "directory": confuse.Optional(
                confuse.Filename(cwd=os.getcwd()) if not output_dir_relative_to_config
                else confuse.Filename(in_source_dir=True)),
            "relative_to_config": bool
        },
        "logging": {
            "level": confuse.OneOf(["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"])
        },
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
    include_undocumented_cpp_member: bool = True
    include_undocumented_ct_add_test: bool = True
    include_undocumented_ct_add_section: bool = True
    recursive: bool = False


@dataclass
class OutputSettings:
    directory: str = None
    relative_to_config: bool = False


@dataclass
class LoggingSettings:
    level: str = "INFO"


@dataclass
class RSTSettings:
    file_extensions_in_titles: bool = False
    file_extensions_in_modules: bool = False
    prefix: str = None
    module_path_separator: str = "."
    headers: List[str] = ('#', '*', '=', '-', '_', '~', '!', '&', '@', '^')


@dataclass
class Settings:
    input: InputSettings = InputSettings()
    output: OutputSettings = OutputSettings()
    logging: LoggingSettings = LoggingSettings()
    rst: RSTSettings = RSTSettings()


def dict_to_settings(input_dict: dict):
    input_settings = InputSettings(**input_dict["input"])
    output_settings = OutputSettings(**input_dict["output"])
    logging_settings = LoggingSettings(**input_dict["logging"])
    rst_settings = RSTSettings(**input_dict["rst"])
    return Settings(input_settings, output_settings, logging_settings, rst_settings)
