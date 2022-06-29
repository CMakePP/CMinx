import confuse

config_template = {
    "input": {
        "include_undocumented_functions": True,
        "include_undocumented_macros": True,
        "include_undocumented_classes": True,
        "include_undocumented_attributes": True,
        "include_undocumented_members": True,
        "recursive": False
    },
    "output": {
        "file_extensions_in_titles": False,
        "file_extensions_in_modules": False,
        "module_path_separator": ".",
        "directory": confuse.Optional(confuse.Filename())
    },
    "logging": {
        "level": confuse.OneOf(["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"])
    },
    "rst": {
        "headers": confuse.StrSeq(),
        "prefix": confuse.Optional(confuse.String())
    }

}
