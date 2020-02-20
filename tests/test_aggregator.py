#!/usr/bin/python3
import context
import unittest
import sys
from antlr4 import *
from cmakedoc.parser.CMakeLexer import CMakeLexer
from cmakedoc.parser.CMakeParser import CMakeParser
from cmakedoc.parser.CMakeListener import CMakeListener
from cmakedoc.parser.aggregator import DocumentationAggregator, DOC_TYPES, FunctionDocumentation, MacroDocumentation, VariableDocumentation, VarType
from cmakedoc.parser import ParserErrorListener, CMakeSyntaxError


class TestAggregator(unittest.TestCase):

    def setUp(self):
        self.filename = "test_samples/example.cmake"
        #We need a string stream of some kind, FileStream is easiest
        self.input_stream = FileStream(self.filename)
        self.reset()

    def reset(self):
        #Convert those strings into tokens and build a stream from those
        self.lexer = CMakeLexer(self.input_stream)
        self.stream = CommonTokenStream(self.lexer)

        #We now have a stream of CommonToken instead of strings, parsers require this type of stream
        self.parser = CMakeParser(self.stream)
        self.parser.addErrorListener( ParserErrorListener() )
        self.tree = self.parser.cmake_file()

        #Hard part is done, we now have a fully useable parse tree, now we just need to walk it
        self.aggregator = DocumentationAggregator()
        self.walker = ParseTreeWalker()
        self.walker.walk(self.aggregator, self.tree)


    def test_aggregated_docs(self):

        #All of the documented commands are now stored in aggregator.documented,
        #each element is a namedtuple repesenting the type of documentation it is.
        #So far we can document functions, macros, and variables (only strings and lists built using set)
        for doced_command in self.aggregator.documented:
             self.assertNotEqual(doced_command, None)
             self.assertIn(type(doced_command), DOC_TYPES, "Unknown documentation type")

    def test_doccomment_function_leading_space(self):
        docstring = "This is a function"
        function_name = "TEST_FUNC"
        params = ["param1", "param2"]

        self.input_stream = InputStream(f'''
#[[[
 {docstring}
#]]
function({function_name} {params[0]} {params[1]})

endfunction()
        ''')
        self.reset()
        self.assertEqual(len(self.aggregator.documented), 1, "Different number of documented commands than expected")
        self.assertEqual(type(self.aggregator.documented[0]), FunctionDocumentation, "Unexpected documentation type")
        self.assertEqual(self.aggregator.documented[0].doc.strip(), docstring, "Incorrect docstring extracted")
        self.assertEqual(self.aggregator.documented[0].function.strip(), function_name, "Incorrect function_name extracted")
        self.assertListEqual([param.strip() for param in self.aggregator.documented[0].params], params, "Incorrect params extracted")

    def test_doccomment_macro_leading_space(self):
        docstring = "This is a macro"
        macro_name = "testmacro"
        params = ["param1", "param2"]

        self.input_stream = InputStream(f'''
#[[[
 {docstring}
#]]
macro({macro_name} {params[0]} {params[1]})

endmacro()
        ''')
        self.reset()
        self.assertEqual(len(self.aggregator.documented), 1, "Different number of documented commands than expected")
        self.assertEqual(type(self.aggregator.documented[0]), MacroDocumentation, "Unexpected documentation type")
        self.assertEqual(self.aggregator.documented[0].doc.strip(), docstring, "Incorrect docstring extracted")
        self.assertEqual(self.aggregator.documented[0].macro.strip(), macro_name, "Incorrect macro_name extracted")
        self.assertListEqual([param.strip() for param in self.aggregator.documented[0].params], params, "Incorrect params extracted")

    def test_doccomment_stringvar_leading_space(self):
        docstring = "This is a string variable"
        var_name = "TEST_VAR"
        val = "This is a value"

        self.input_stream = InputStream(f'''
#[[[
 {docstring}
#]]
set({var_name} "{val}")

        ''')
        self.reset()
        self.assertEqual(len(self.aggregator.documented), 1, "Different number of documented commands than expected")
        self.assertEqual(type(self.aggregator.documented[0]), VariableDocumentation, "Unexpected documentation type")
        self.assertEqual(self.aggregator.documented[0].doc.strip(), docstring, "Incorrect docstring extracted")
        self.assertEqual(self.aggregator.documented[0].varname.strip(), var_name, "Incorrect function_name extracted")
        self.assertEqual(self.aggregator.documented[0].type, VarType.String)
        self.assertEqual(self.aggregator.documented[0].value.strip(), val.strip(), "Incorrect value extracted")

    def test_doccomment_listvar_leading_space(self):
        docstring = "This is a list variable"
        var_name = "listvar"
        params = ["param1", "param2"]

        self.input_stream = InputStream(f'''
#[[[
 {docstring}
#]]
set({var_name} {params[0]} {params[1]})
        ''')
        self.reset()
        self.assertEqual(len(self.aggregator.documented), 1, "Different number of documented commands than expected")
        self.assertEqual(type(self.aggregator.documented[0]), VariableDocumentation, "Unexpected documentation type")
        self.assertEqual(self.aggregator.documented[0].doc.strip(), docstring, "Incorrect docstring extracted")
        self.assertEqual(self.aggregator.documented[0].varname.strip(), var_name, "Incorrect var_name extracted")
        self.assertEqual(self.aggregator.documented[0].type, VarType.List)

        self.assertListEqual([param.strip() for param in self.aggregator.documented[0].value], params, "Incorrect list elements extracted")

    def test_unset(self):
        docstring = "Unsetting a variable"
        var_name = "myvar"

        self.input_stream = InputStream(f'''
#[[[
 {docstring}
#]]
set({var_name})
        ''')
        self.reset()
        self.assertEqual(len(self.aggregator.documented), 1, "Different number of documented commands than expected")
        self.assertEqual(type(self.aggregator.documented[0]), VariableDocumentation, "Unexpected documentation type")
        self.assertEqual(self.aggregator.documented[0].doc.strip(), docstring, "Incorrect docstring extracted")
        self.assertEqual(self.aggregator.documented[0].varname.strip(), var_name, "Incorrect var_name extracted")
        self.assertEqual(self.aggregator.documented[0].type, VarType.Unset)


    def test_unknown_documented_command(self):
        self.input_stream = InputStream('#[[[\nThis is documentation for an unknown command\n#]]\nimport_guard()')
        with self.assertRaises(NotImplementedError):
            self.reset()

if __name__ == '__main__':
    unittest.main()
