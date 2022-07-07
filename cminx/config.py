import confuse
from typing import List
from dataclasses import dataclass

config_template = {
    "input": {
        "include_undocumented_function": True,
        "include_undocumented_macro": True,
        "include_undocumented_cpp_class": True,
        "include_undocumented_cpp_attr": True,
        "include_undocumented_cpp_member": True,
        "recursive": False
    },
    "output": confuse.Optional({
        "directory": confuse.Optional(confuse.Filename(in_source_dir=True))
    }, default={"directory": None}),
    "logging": {
        "level": confuse.OneOf(["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"])
    },
    "rst": {
        "file_extensions_in_titles": False,
        "file_extensions_in_modules": False,
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
    recursive: bool = False


@dataclass
class OutputSettings:
    directory: str = None


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
