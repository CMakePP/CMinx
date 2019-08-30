from .cmake_regexer import CMakeRegexer
from .parse_block_comment import parse_block_comment, parse_block_docstring
from .parse_signature import parse_function_start, parse_macro_start
from .parse_single_line import parse_single_line_comment, \
    parse_single_line_docstring, parse_blank_line, parse_other_line


class Parser:

    def __init__(self):
        """Register the default handlers with the Parser instance."""

        self.handlers = {
            'function start': parse_function_start,
            'macro start': parse_macro_start,
            'single line comment': parse_single_line_comment,
            'single line docstring': parse_single_line_docstring,
            'block docstring': parse_block_docstring,
            'block comment start': parse_block_comment,
            'blank': parse_blank_line,
            'other': parse_other_line
        }

    def parse(self, lines):

        regexer = CMakeRegexer()
        content = []

        while lines:
            nlines = len(lines)
            purpose = regexer.get_purpose(lines[0])

            if purpose not in self.handlers:
                raise KeyError('Handler for ' + purpose + ' not found. If you '
                               'are a user, this is likely caused by a syntax '
                               'error in your CMake code. Ensure your CMake '
                               'code runs. If you are a developer, did you add '
                               'a new  "purpose" and forget to register a '
                               'corresponding handler with the Parser class?')
            
            data, lines = self.handlers[purpose](lines)
            content.append((purpose, data))

            if len(lines) == nlines:  # pragma: no cover
                raise RuntimeError('Developer error: handler did not advance '
                                   'buffer to the next line.')

        return content
