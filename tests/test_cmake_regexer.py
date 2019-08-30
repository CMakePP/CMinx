import context  # Sets up PYTHON_PATH for this test
from cmakedoc.cmake_regexer import CMakeRegexer as CMakeRegexer
import unittest


class TestCMakeRegexer(unittest.TestCase):
    def setUp(self):
        self.strs2test = {
            "function start": ["function(", " function(", " FUNCTION("],
            "function end": ["endfunction()", " endfunction()",
                              "ENDFUNCTION()", "endfunction( )"],
            "macro start": ["macro(", " macro(", " MACRO("],
            "macro end": ["endmacro()", " endmacro()", "ENDMACRO()",
                           "endmacro( )"],
            "single line comment": ["#hi", " #hi", "# hi", " # hi"],
            "single line docstring": ["##hi", " ##hi", "## hi", " ## hi"],
            "block comment start": ["#[[", " #[[", " #[[ "],
            "block comment end": ["#]]", " #]]", " #]] "],
            "blank": ["", "\n", "    ", "    \n"],
            "other": ["set(var value)", "file(stuff)"]
        }
        self.regexer = CMakeRegexer()

    def test_get_purpose(self):
        for type_i, strs_i in self.strs2test.items():
            for str_i in strs_i:
                msg = 'type: "{}" str: "{}"'.format(type_i, str_i)
                with self.subTest(msg):
                    self.assertEqual(type_i, self.regexer.get_purpose(str_i))

    def test_has_purpose(self):
        regexer = self.regexer
        for type_i, strs_i in self.strs2test.items():
            for str_i in strs_i:
                for type_j in self.strs2test.keys():
                    if type_j == 'other':
                        continue
                    msg = 'purpose: "{}" str: "{}"'.format(type_j, str_i)
                    with self.subTest(msg):
                        if type_i == type_j:
                            self.assertTrue(regexer.has_purpose(str_i, type_j))
                        else:
                            self.assertFalse(regexer.has_purpose(str_i, type_j))

    def test_has_purpose_bad_type(self):
        self.assertRaises(ValueError, self.regexer.has_purpose, '##',
                          'not a real type')


if __name__ == '__main__':
    unittest.main()
