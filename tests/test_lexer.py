import context  # Sets up PYTHON_PATH for this test
from cmakedoc.parser.CMakeLexer import CMakeLexer
from antlr4 import InputStream
import unittest

#TODO Adapt old tests to new framework

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
        self.assertListEqual([token.type for token in self.tokens], [CMakeLexer.Bracket_doccomment])
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
