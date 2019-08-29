from cmake_regexer import CMakeRegexer
import parse_block_comment
from parse_signature import parse_function_start, parse_macro_start

class Parser:

    def __init__(self):
        self.parsers = {
            "function start": parse_function_start,
            "macro start" : parse_macro_start,
            "block comment start": parse_block_comment
        }

    def parse(self, file):
        lines = file.splitlines()
        regexer = CMakeRegexer()
        content = []

        while lines:
            purpose = regexer.get_purpose(lines[0])
            data, lines = self.parsers[purpose](lines)
            content.append((purpose, data))



