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
import unittest

from antlr4 import *
from antlr4.error.Errors import InputMismatchException

from cminx.parser import ParserErrorListener, CMakeSyntaxError
from cminx.parser.CMakeLexer import CMakeLexer
from cminx.parser.CMakeListener import CMakeListener
from cminx.parser.CMakeParser import CMakeParser


class MockListener(CMakeListener):
    def __init__(self):
        self.elements = []
        """List of parsed element contexts. such as commands and documented commands"""

    def enterDocumented_command(self, ctx: CMakeParser.Documented_commandContext):
        self.elements.append(ctx)

    def enterCommand_invocation(self, ctx: CMakeParser.Command_invocationContext):
        self.elements.append(ctx)


class TestParser(unittest.TestCase):
    def setUp(self):
        self.input_stream = InputStream("")
        self.reset()

    def reset(self):
        # Convert those strings into tokens and build a stream from those
        self.lexer = CMakeLexer(self.input_stream)
        self.stream = CommonTokenStream(self.lexer)

        # We now have a stream of CommonToken instead of strings, parsers require this type of stream
        self.parser = CMakeParser(self.stream)
        self.parser.removeErrorListeners()
        self.parser.addErrorListener(ParserErrorListener())
        self.tree = self.parser.cmake_file()

        # Hard part is done, we now have a fully useable parse tree, now we just need to walk it
        self.aggregator = MockListener()
        self.walker = ParseTreeWalker()
        self.walker.walk(self.aggregator, self.tree)

    def test_empty(self):
        self.reset()
        self.assertEqual(self.aggregator.elements, [])

    def test_function_single_arg(self):
        self.input_stream = InputStream('''
function(MyFunction arg1)\n    message("${arg1}")\nendfunction()
        ''')
        self.reset()
        self.assertEqual(len(self.aggregator.elements), 3, "Different number of extracted elements")
        for element in self.aggregator.elements:
            self.assertEqual(type(element), CMakeParser.Command_invocationContext)
        for i in range(0, len(self.aggregator.elements)):
            element = self.aggregator.elements[i]
            if i == 0:
                # function() command
                self.assertEqual(element.Identifier().getText().lower(), "function")
                self.assertEqual(element.single_argument()[0].Identifier().getText(), "MyFunction")
                params = [param.Identifier().getText() for param in
                          element.single_argument()[1:]]  # Extract declared function parameters
                self.assertListEqual(params, ["arg1"])
            elif i == 1:
                # message() command
                self.assertEqual(element.Identifier().getText().lower(), "message")
                params = [param.Quoted_argument().getText() for param in
                          element.single_argument()]  # Extract message() params
                self.assertListEqual(params, ['"${arg1}"'])
            elif i == 2:
                # endfunction() command
                self.assertEqual(element.Identifier().getText().lower(), "endfunction")
                params = element.single_argument()
                self.assertEqual(params, [])

    def test_function_multi_arg(self):
        self.input_stream = InputStream('''
function(MyFunction arg1 arg2)\n    message("${arg1}" "${arg2}")\nendfunction()
        ''')
        self.reset()
        self.assertEqual(len(self.aggregator.elements), 3, "Different number of extracted elements")
        for element in self.aggregator.elements:
            self.assertEqual(type(element), CMakeParser.Command_invocationContext)
        for i in range(0, len(self.aggregator.elements)):
            element = self.aggregator.elements[i]
            if i == 0:
                # function() command
                self.assertEqual(element.Identifier().getText().lower(), "function")
                self.assertEqual(element.single_argument()[0].Identifier().getText(), "MyFunction")
                params = [param.Identifier().getText() for param in
                          element.single_argument()[1:]]  # Extract declared function parameters
                self.assertListEqual(params, ["arg1", "arg2"])
            elif i == 1:
                # message() command
                self.assertEqual(element.Identifier().getText().lower(), "message")
                params = [param.Quoted_argument().getText() for param in
                          element.single_argument()]  # Extract message() params
                self.assertListEqual(params, ['"${arg1}"', '"${arg2}"'])
            elif i == 2:
                # endfunction() command
                self.assertEqual(element.Identifier().getText().lower(), "endfunction")
                params = element.single_argument()
                self.assertEqual(params, [])

    def test_no_ending_paren(self):
        with self.assertRaises(CMakeSyntaxError):
            self.input_stream = InputStream('''
function(TEST
            ''')
            self.reset()

    def test_mismatch(self):
        with self.assertRaises(InputMismatchException):
            self.input_stream = InputStream('''
()
                ''')
            self.reset()


if __name__ == '__main__':
    unittest.main()
