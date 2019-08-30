import context  # Sets up PYTHON_PATH for this test
import cmakedoc.parse_signature as ps
import unittest


class TestParseSignature(unittest.TestCase):
    def test_no_closing_parenthesis_simple(self):
        lines = 'function(my_function arg1'.splitlines()
        self.assertRaises(SyntaxError, ps._parse_signature, 'function', lines)

    def test_no_closing_parenthesis_hard(self):
        lines = 'function(my_function arg1\nendfunction()'.splitlines()
        self.assertRaises(SyntaxError, ps._parse_signature, 'function', lines)

    def test_no_end(self):
        lines = 'function(my_function arg1)\n'.splitlines()
        self.assertRaises(SyntaxError, ps._parse_signature, 'function', lines)

    def test_simple_signature(self):
        lines = 'macro(my_macro arg1)\nset(x ${arg1})\nendmacro()'.splitlines()
        data, lines = ps._parse_signature('macro', lines)
        self.assertEqual(data, 'macro(my_macro arg1)')
        self.assertEqual(lines, [])

    def test_multiline_signature(self):
        lines = 'macro(my_macro\narg1\n)\nset(x ${arg1})\nendmacro()'
        lines = lines.splitlines()
        data, lines = ps._parse_signature('macro', lines)
        self.assertEqual(data, 'macro(my_macro\narg1\n)')
        self.assertEqual(lines, [])

    def test_stuff_after_signature(self):
        lines = 'macro(my_macro arg1)\nset(x ${arg1})\nendmacro()\nhello world'
        lines = lines.splitlines()
        data, lines = ps._parse_signature('macro', lines)
        self.assertEqual(data, 'macro(my_macro arg1)')
        self.assertEqual(lines, ['hello world'])


class TestParseFunctionStart(unittest.TestCase):
    def test_not_function(self):
        self.assertRaises(ValueError, ps.parse_function_start, ['Hello World'])

    def test_function(self):
        lines = 'function(my_fxn arg1)\nendfunction()'.splitlines()
        data, lines = ps.parse_function_start(lines)
        self.assertEqual(data, 'function(my_fxn arg1)')
        self.assertEqual(lines, [])


class TestParseMacroStart(unittest.TestCase):
    def test_not_function(self):
        self.assertRaises(ValueError, ps.parse_macro_start, ['Hello World'])

    def test_macro(self):
        lines = 'macro(my_macro arg1)\nendmacro()'.splitlines()
        data, lines = ps.parse_macro_start(lines)
        self.assertEqual(data, 'macro(my_macro arg1)')
        self.assertEqual(lines, [])


if __name__ == '__main__':
    unittest.main()
