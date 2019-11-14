import context  # Sets up PYTHON_PATH for this test
#import cmakedoc.parse_single_line as pslc
import unittest

#TODO Adapt old tests to new framework
"""
class TestParseLineComment(unittest.TestCase):
    def setUp(self):
        self.slc = 'single line comment'
        self.sld = 'single line docstring'

    def test_empty_lines(self):
        self.assertRaises(ValueError, pslc._parse_single_line, self.slc, [])

    def test_only_comment(self):
        lines = '#hello world'.splitlines()
        data, lines = pslc._parse_single_line(self.slc, lines)
        self.assertEqual(data, '#hello world')
        self.assertEqual(lines, [])

    def test_comment_followed_by_stuff(self):
        lines = '##hello world\nother stuff'.splitlines()
        data, lines = pslc._parse_single_line(self.sld, lines)
        self.assertEqual(data, '##hello world')
        self.assertEqual(lines, ['other stuff'])

    def test_multiline_comment(self):
        lines = '##hello world\n##hello bob'.splitlines()
        data, lines = pslc._parse_single_line(self.sld, lines)
        self.assertEqual(data, '##hello world\n##hello bob')
        self.assertEqual(lines, [])

    def test_only_grab_same_comment_char(self):
        lines = '##hello world\n#hello bob'.splitlines()
        data, lines = pslc._parse_single_line(self.sld, lines)
        self.assertEqual(data, '##hello world')
        self.assertEqual(lines, ['#hello bob'])


class TestParseSingleLineComment(unittest.TestCase):
    def test_non_single_line_comment(self):
        self.assertRaises(ValueError, pslc.parse_single_line_comment, ['hi'])

    def test_single_line_comment(self):
        data, lines = pslc.parse_single_line_comment(['#Hello world'])
        self.assertEqual(data, '#Hello world')
        self.assertEqual(lines, [])


class TestParseSingleLineDocstring(unittest.TestCase):
    def test_not_single_line_docstring(self):
        self.assertRaises(ValueError, pslc.parse_single_line_docstring, ['hi'])

    def test_single_line_docstring(self):
        data, lines = pslc.parse_single_line_docstring(['##Hello world'])
        self.assertEqual(data, '##Hello world')
        self.assertEqual(lines, [])


class TestParseOtherLine(unittest.TestCase):
    def test_not_other_line(self):
        self.assertRaises(ValueError, pslc.parse_other_line, ['#hi'])

    def test_other_line(self):
        data, lines = pslc.parse_other_line(['set(x hello world)'])
        self.assertEqual(data, 'set(x hello world)')
        self.assertEqual(lines, [])


class TestParseBlankLine(unittest.TestCase):
    def test_not_blank_line(self):
        self.assertRaises(ValueError, pslc.parse_blank_line, ['#hi'])

    def test_blank_line(self):
        data, lines = pslc.parse_blank_line(['   '])
        self.assertEqual(data, '   ')
        self.assertEqual(lines, [])

"""
if __name__ == '__main__':
    unittest.main()
