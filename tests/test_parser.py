import context
from cmakedoc.parser.CMakeParser import CMakeParser
import unittest



"""
class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_bad_purpose(self):
        self.assertRaises(KeyError, self.parser.parse, ['endfunction()'])

    def test_empty(self):
        content = self.parser.parse([])
        self.assertEqual(content, [])

    def test_function_start(self):
        lines = 'function(my_fxn arg1)\nendfunction()'.splitlines()
        content = self.parser.parse(lines)
        self.assertEqual(content, [('function start', 'function(my_fxn arg1)')])

    def test_macro_start(self):
        lines = 'macro(my_macro arg1)\nendmacro()'.splitlines()
        content = self.parser.parse(lines)
        self.assertEqual(content, [('macro start', 'macro(my_macro arg1)')])

    def test_single_line_comment(self):
        lines = ['# Hello world']
        content = self.parser.parse(lines)
        self.assertEqual(content, [('single line comment', '# Hello world')])

    def test_single_line_docstring(self):
        lines = ['## Hello world']
        content = self.parser.parse(lines)
        self.assertEqual(content, [('single line docstring', '## Hello world')])

    def test_block_docstring(self):
        comment = '#[[[\nHello world\n#]]'
        lines = comment.splitlines()
        content = self.parser.parse(lines)
        self.assertEqual(content, [('block docstring', comment)])

    def test_block_comment_start(self):
        comment = '#[[\nHello world\n#]]'
        lines = comment.splitlines()
        content = self.parser.parse(lines)
        self.assertEqual(content, [('block comment start', comment)])

    def test_blank(self):
        lines = '\n\n\n'.splitlines()
        content = self.parser.parse(lines)
        self.assertEqual(content, [('blank', '\n\n')])

    def test_other(self):
        lines = 'set(x hello)\nset(y world)'.splitlines()
        content = self.parser.parse(lines)
        self.assertEqual(content, [('other', 'set(x hello)\nset(y world)')])

"""
if __name__ == '__main__':
    unittest.main()
