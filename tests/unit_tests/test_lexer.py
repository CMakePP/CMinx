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

from antlr4 import InputStream

from cminx.parser.CMakeLexer import CMakeLexer


# TODO Adapt old tests to new framework

class TestLexer(unittest.TestCase):
    def setUp(self):
        self.stream = InputStream("")
        self.reset()

    def reset(self):
        self.lexer = CMakeLexer(self.stream)
        self.tokens = self.lexer.getAllTokens()

    def test_empty_lines(self):
        self.assertListEqual([], self.tokens)

    def test_line_comment(self):
        self.stream = InputStream('#This is a line comment')
        self.reset()
        self.assertListEqual([], self.tokens)

    def test_block_comment(self):
        self.stream = InputStream('#[[This is a block comment#]]')
        self.reset()
        self.assertListEqual([], self.tokens)

    def test_block_doccomment(self):
        doc = '#[[[\nThis is a doccomment\n#]]'
        self.stream = InputStream(doc)
        self.reset()
        self.assertListEqual([token.type for token in self.tokens], [CMakeLexer.Docstring])
        self.assertEqual(self.tokens[0].text, doc)

    def test_identifier(self):
        doc = 'function'
        self.stream = InputStream(doc)
        self.reset()
        self.assertListEqual([token.type for token in self.tokens], [CMakeLexer.Identifier])
        self.assertEqual(self.tokens[0].text, doc)

    def test_quoted_argument(self):
        doc = '"This is a quoted argument"'
        self.stream = InputStream(doc)
        self.reset()
        self.assertListEqual([token.type for token in self.tokens], [CMakeLexer.Quoted_argument])
        self.assertEqual(self.tokens[0].text, doc)


if __name__ == '__main__':
    unittest.main()
