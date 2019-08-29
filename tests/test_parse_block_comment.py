import context
import cmakedoc.parse_block_comment as pbc
import unittest


class TestParseCommentBlock(unittest.TestCase):
    def test_empty_lines(self):
        self.assertRaises(ValueError, pbc._parse_comment_block, [])

    def test_no_block_end(self):
        lines = '#[[\nhello world\n'.splitlines()
        self.assertRaises(SyntaxError, pbc._parse_comment_block, lines)

    def test_only_block(self):
        lines = '#[[\nhello world\n#]]'.splitlines()
        data, lines = pbc._parse_comment_block(lines)
        self.assertEqual(data, '#[[\nhello world\n#]]')
        self.assertEqual(lines, [])

    def test_block_followed_by_stuff(self):
        lines = '#[[[\nhello world\n#]]\nother stuff'.splitlines()
        data, lines = pbc._parse_comment_block(lines)
        self.assertEqual(data, '#[[[\nhello world\n#]]')
        self.assertEqual(lines, ['other stuff'])


class TestParseBlockComment(unittest.TestCase):
    def test_non_block_comment_start(self):
        self.assertRaises(ValueError, pbc.parse_block_comment, ['hi'])


class TestParseBlockDocstring(unittest.TestCase):
    def test_non_block_docstring_start(self):
        self.assertRaises(ValueError, pbc.parse_block_comment, ['hi'])


if __name__ == '__main__':
    unittest.main()
