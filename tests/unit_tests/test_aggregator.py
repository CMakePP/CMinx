#!/usr/bin/python3
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

import pytest

import context
from antlr4 import *

from cminx.exceptions import CMakeSyntaxException
from cminx.parser import ParserErrorListener
from cminx.parser.CMakeLexer import CMakeLexer
from cminx.parser.CMakeParser import CMakeParser
from cminx.aggregator import DocumentationAggregator
from cminx.documentation_types import FunctionDocumentation, MacroDocumentation, VariableDocumentation, \
    GenericCommandDocumentation, ClassDocumentation, VarType, DocumentationType


class TestAggregator(unittest.TestCase):

    def setUp(self):
        self.filename = context.example_cmake
        # We need a string stream of some kind, FileStream is easiest
        self.input_stream = FileStream(self.filename)
        self.reset()

    def reset(self):
        # Convert those strings into tokens and build a stream from those
        self.lexer = CMakeLexer(self.input_stream)
        self.stream = CommonTokenStream(self.lexer)

        # We now have a stream of CommonToken instead of strings, parsers require this type of stream
        self.parser = CMakeParser(self.stream)
        self.parser.addErrorListener(ParserErrorListener())
        self.tree = self.parser.cmake_file()

        # Hard part is done, we now have a fully useable parse tree, now we just need to walk it
        self.aggregator = DocumentationAggregator()
        self.walker = ParseTreeWalker()
        self.walker.walk(self.aggregator, self.tree)

    def test_aggregated_docs(self):

        # All of the documented commands are now stored in aggregator.documented,
        # each element is a namedtuple repesenting the type of documentation it is.
        # So far we can document functions, macros, and variables (only strings and lists built using set)
        for doced_command in self.aggregator.documented:
            self.assertNotEqual(doced_command, None)
            self.assertIsInstance(doced_command, DocumentationType, "Unknown documentation type")

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
        self.assertEqual(self.aggregator.documented[0].name.strip(), function_name,
                         "Incorrect function_name extracted")
        self.assertListEqual([param.strip() for param in self.aggregator.documented[0].params], params,
                             "Incorrect params extracted")

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
        self.assertEqual(self.aggregator.documented[0].name.strip(), macro_name, "Incorrect macro_name extracted")
        self.assertListEqual([param.strip() for param in self.aggregator.documented[0].params], params,
                             "Incorrect params extracted")

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
        self.assertEqual(self.aggregator.documented[0].name.strip(), var_name, "Incorrect function_name extracted")
        self.assertEqual(self.aggregator.documented[0].type, VarType.STRING)
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
        self.assertEqual(self.aggregator.documented[0].name.strip(), var_name, "Incorrect var_name extracted")
        self.assertEqual(self.aggregator.documented[0].type, VarType.LIST)

        self.assertEqual(self.aggregator.documented[0].value, " ".join(params),
                         "Incorrect list elements extracted")

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
        self.assertEqual(self.aggregator.documented[0].name.strip(), var_name, "Incorrect var_name extracted")
        self.assertEqual(self.aggregator.documented[0].type, VarType.UNSET)

    def test_cpp_class_no_superclass_no_inner(self):
        self.test_cpp_class_multi_superclass_no_inner([])

    def test_cpp_class_multi_superclass_multi_members(self,
                                                      superclasses=("SuperClassA", "SuperClassB", "SuperClassC"),
                                                      attributes=("attr1", "attr2"),
                                                      methods=("method1", "method2"),
                                                      inner_classes=("Inner1", "Inner2")):
        class_docstring = "This is a class"
        inner_class_docstring = "#[[[\n# This is an inner class\n#]]"
        method_docstring = "#[[[\n# This is a method\n#]]"
        attribute_docstring = "#[[[\n# This is an attribute\n#]]"
        class_name = "MyClass"
        inner_class_definitions = '\n'.join(
            [f'{inner_class_docstring}\ncpp_class({inner_class_name})\ncpp_end_class()' for inner_class_name in
             inner_classes])
        method_definitions = '\n'.join([
            f'{method_docstring}\ncpp_member({method_name} {class_name})\nfunction(' + '${' + method_name + '})\nendfunction()'
            for method_name in methods])
        attribute_definitions = '\n'.join(
            [f'{attribute_docstring}\ncpp_attr({class_name} {attr_name})' for attr_name in attributes])
        self.input_stream = InputStream(f'''
#[[[
# {class_docstring}
#]]
cpp_class({class_name} {' '.join(superclasses)})

    {attribute_definitions}

    {method_definitions}

    {inner_class_definitions}

cpp_end_class()
        ''')
        self.reset()
        self.assertEqual(len(self.aggregator.documented), 1 + len(inner_classes),
                         "Different number of documented commands than expected")
        self.assertEqual(type(self.aggregator.documented[0]), ClassDocumentation, "Unexpected documentation type")
        self.assertEqual(self.aggregator.documented[0].doc.strip(), class_docstring, "Incorrect docstring extracted")
        self.assertEqual(self.aggregator.documented[0].name.strip(), class_name, "Incorrect class name extracted")
        self.assertEqual(len(self.aggregator.documented[0].superclasses), len(superclasses),
                         "Superclasses incorrectly found")
        for i in range(len(superclasses)):
            self.assertEqual(self.aggregator.documented[0].superclasses[i].strip(), superclasses[i].strip(),
                             "Superclass name not preserved")

        self.assertEqual(len(self.aggregator.documented[0].inner_classes), len(inner_classes),
                         "Inner classes incorrectly found")
        self.assertEqual(len(self.aggregator.documented[0].members), len(methods), "Members incorrectly found")
        self.assertEqual(len(self.aggregator.documented[0].attributes), len(attributes), "Attributes incorrectly found")

    def test_cpp_class_multi_superclass_no_inner(self, superclasses=["SuperClassA", "SuperClassB", "SuperClassC"]):
        self.test_cpp_class_multi_superclass_multi_members(superclasses=superclasses, attributes=[], methods=[])

    def test_cpp_class_one_superclasses_no_inner(self):
        self.test_cpp_class_multi_superclass_no_inner(["SuperClass"])

    def test_unknown_documented_command(self):
        docstring = 'This is documentation for an unknown command'
        params = ["FATAL_ERROR", "\"This is a test\""]
        command_name = "message"
        command = f'{command_name}({" ".join(params)})'
        self.input_stream = InputStream(f'#[[[\n{docstring}\n#]]\n{command}')
        self.reset()
        self.assertEqual(len(self.aggregator.documented), 1, "Different number of documented commands than expected")
        self.assertEqual(type(self.aggregator.documented[0]), GenericCommandDocumentation,
                         "Unexpected documentation type")
        self.assertEqual(self.aggregator.documented[0].doc.strip(), docstring, "Incorrect docstring extracted")
        self.assertEqual(self.aggregator.documented[0].name.strip(), command_name, "Incorrect command name extracted")
        for i in range(0, len(params)):
            p = self.aggregator.documented[0].params[i]
            self.assertEqual(params[i], p, "Incorrect command parameters. Expected {params[i]}, got {p}")

    def test_incorrect_function_params(self):
        docstring = "This is documentation for an incorrect function() call"
        params = []
        command_name = "function"
        command = f'{command_name}({" ".join(params)})'
        self.input_stream = InputStream(f'#[[[\n{docstring}\n#]]\n{command}')
        with pytest.raises(CMakeSyntaxException):
            self.reset()
        self.assertEqual(0, len(self.aggregator.documented),
                         f"Incorrect {command_name}() call was still added to documented list: {self.aggregator.documented}")

    def test_incorrect_macro_params(self):
        docstring = "This is documentation for an incorrect macro() call"
        params = []
        command_name = "macro"
        command = f'{command_name}({" ".join(params)})'
        self.input_stream = InputStream(f'#[[[\n{docstring}\n#]]\n{command}')
        with pytest.raises(CMakeSyntaxException):
            self.reset()
        self.assertEqual(0, len(self.aggregator.documented),
                         f"Incorrect {command_name}() call was still added to documented list: {self.aggregator.documented}")

    def test_incorrect_ct_add_test_params(self):
        docstring = "This is documentation for an incorrect ct_add_test() call"
        # ct_add_test() requires an additional param after NAME
        params = ["NAME"]
        command_name = "ct_add_test"
        command = f'{command_name}({" ".join(params)})'
        self.input_stream = InputStream(f'#[[[\n{docstring}\n#]]\n{command}')
        self.reset()
        self.assertEqual(0, len(self.aggregator.documented),
                         f"Incorrect {command_name}() call was still added to documented list: {self.aggregator.documented}")

    def test_invalid_ct_add_test_params(self):
        docstring = "This is documentation for an incorrect ct_add_section() call"
        # ct_add_test() requires an additional param after NAME, not before
        params = ["test_name", "NAME"]
        command_name = "ct_add_test"
        command = f'{command_name}({" ".join(params)})'
        self.input_stream = InputStream(f'#[[[\n{docstring}\n#]]\n{command}')
        self.reset()
        self.assertEqual(0, len(self.aggregator.documented),
                         f"Incorrect {command_name}() call was still added to documented list: {self.aggregator.documented}")

    def test_incorrect_ct_add_section_params(self):
        docstring = "This is documentation for an incorrect ct_add_section() call"
        # ct_add_section() requires an additional param after NAME
        params = ["NAME"]
        command_name = "ct_add_section"
        command = f'{command_name}({" ".join(params)})'
        self.input_stream = InputStream(f'#[[[\n{docstring}\n#]]\n{command}')
        self.reset()
        self.assertEqual(0, len(self.aggregator.documented),
                         f"Incorrect {command_name}() call was still added to documented list: {self.aggregator.documented}")

    def test_invalid_ct_add_section_params(self):
        docstring = "This is documentation for an incorrect ct_add_section() call"
        # ct_add_section() requires an additional param after NAME, not before
        params = ["section_name", "NAME"]
        command_name = "ct_add_section"
        command = f'{command_name}({" ".join(params)})'
        self.input_stream = InputStream(f'#[[[\n{docstring}\n#]]\n{command}')
        self.reset()
        self.assertEqual(0, len(self.aggregator.documented),
                         f"Incorrect {command_name}() call was still added to documented list: {self.aggregator.documented}")

    def test_invalid_ctest_add_test_params(self):
        docstring = "This is documentation for an incorrect ct_add_section() call"
        # add_test() requires two params minimum
        params = ["NAME"]
        command_name = "add_test"
        command = f'{command_name}({" ".join(params)})'
        self.input_stream = InputStream(f'#[[[\n{docstring}\n#]]\n{command}')
        self.reset()
        self.assertEqual(0, len(self.aggregator.documented),
                         f"Incorrect {command_name}() call was still added to documented list: {self.aggregator.documented}")

    def test_incorrect_ctest_add_test_params(self):
        docstring = "This is documentation for an incorrect ct_add_section() call"
        # add_test() requires an additional param after NAME, not before
        params = ["blah", "NAME"]
        command_name = "add_test"
        command = f'{command_name}({" ".join(params)})'
        self.input_stream = InputStream(f'#[[[\n{docstring}\n#]]\n{command}')
        self.reset()
        self.assertEqual(0, len(self.aggregator.documented),
                         f"Incorrect {command_name}() call was still added to documented list: {self.aggregator.documented}")

    def test_incorrect_set_params(self):
        docstring = "This is documentation for an incorrect set() call"
        params = []
        command_name = "set"
        command = f'{command_name}({" ".join(params)})'
        self.input_stream = InputStream(f'#[[[\n{docstring}\n#]]\n{command}')
        self.reset()
        self.assertEqual(0, len(self.aggregator.documented),
                         f"Incorrect {command_name}() call was still added to documented list: {self.aggregator.documented}")

    def test_incorrect_cpp_class_params(self):
        params = []
        command_name = "cpp_class"
        command = f'{command_name}({" ".join(params)})'
        docstring = f"This is documentation for an incorrect {command_name}() call"
        self.input_stream = InputStream(f'#[[[\n{docstring}\n#]]\n{command}')
        self.reset()
        self.assertEqual(0, len(self.aggregator.documented),
                         f"Incorrect {command_name}() call was still added to documented list: {self.aggregator.documented}")

    def test_incorrect_cpp_member_params(self):
        params = []
        command_name = "cpp_member"
        command = f'{command_name}({" ".join(params)})'
        docstring = f"This is documentation for an incorrect {command_name}() call"
        self.input_stream = InputStream(f'#[[[\n{docstring}\n#]]\n{command}')
        self.reset()
        self.assertEqual(0, len(self.aggregator.documented),
                         f"Incorrect {command_name}() call was still added to documented list: {self.aggregator.documented}")

    def test_incorrect_cpp_attribute_params(self):
        params = []
        command_name = "cpp_attr"
        command = f'{command_name}({" ".join(params)})'
        docstring = f"This is documentation for an incorrect {command_name}() call"
        self.input_stream = InputStream(f'#[[[\n{docstring}\n#]]\n{command}')
        self.reset()
        self.assertEqual(0, len(self.aggregator.documented),
                         f"Incorrect {command_name}() call was still added to documented list: {self.aggregator.documented}")

    def test_incorrect_option_params(self):
        params = []
        command_name = "option"
        command = f'{command_name}({" ".join(params)})'
        docstring = f"This is documentation for an incorrect {command_name}() call"
        self.input_stream = InputStream(f'#[[[\n{docstring}\n#]]\n{command}')
        self.reset()
        self.assertEqual(0, len(self.aggregator.documented),
                         f"Incorrect {command_name}() call was still added to documented list: {self.aggregator.documented}")

    def test_cpp_attr_outside_class(self):
        self.input_stream = InputStream("#[[[\n# cpp_attr() outside class\n#]]\ncpp_attr()")
        self.reset()
        self.assertEqual(0, len(self.aggregator.documented),
                         f"cpp_attr() call outside class was still added to documented list: {self.aggregator.documented}")

    def test_cpp_member_outside_class(self):
        self.input_stream = InputStream("#[[[\n# cpp_member() outside class\n#]]\ncpp_member()")
        self.reset()
        self.assertEqual(0, len(self.aggregator.documented),
                         f"cpp_member() call outside class was still added to documented list: {self.aggregator.documented}")

    def test_invalid_syntax(self):
        self.input_stream = InputStream("#[[[\n#invalid syntax\n#]]\nfunction()\nend_function()")
        with pytest.raises(CMakeSyntaxException):
            self.reset()


if __name__ == '__main__':
    unittest.main()
