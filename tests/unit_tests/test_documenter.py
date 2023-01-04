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

import context

from cminx.documenter import Documenter
from cminx.documentation_types import FunctionDocumentation, MacroDocumentation, VariableDocumentation, \
    GenericCommandDocumentation, ClassDocumentation, TestDocumentation, SectionDocumentation, CTestDocumentation, \
    ModuleDocumentation
from cminx.rstwriter import Directive, RSTWriter


class TestDocumenter(unittest.TestCase):

    def setUp(self):
        self.filename = context.example_cmake
        self.reset()

    def reset(self):
        self.documenter = Documenter(self.filename, self.filename)  # File is parsed on __init__

    def test_process(self):
        self.documenter.process()  # Convert all documentation into RST
        self.assertEqual(len(self.documenter.aggregator.documented), len(self.documenter.writer.document) - 1,
                         "Generated RST has different length from input documentation")  # RSTWriter adds one element
        # for document heading, documenter adds another for module definition
        for i in range(0, len(self.documenter.aggregator.documented)):
            doc = self.documenter.aggregator.documented[i]
            element = self.documenter.writer.document[i + 1]
            if isinstance(doc, ModuleDocumentation):
                self.assertIsInstance(element, Directive, "Wrong RST element generated for module doc")
            elif isinstance(doc, FunctionDocumentation):
                self.assertIsInstance(element, Directive, "Wrong RST element generated for function")
                self.assertEqual("function", element.document[0].title, "Wrong directive type for function")
            elif isinstance(doc, MacroDocumentation):
                self.assertIsInstance(element, Directive, "Wrong RST element generated for macro")
                self.assertEqual("function", element.document[0].title, "Wrong directive type for macro")
                self.assertIsInstance(element.document[1], Directive)
                self.assertEqual("note", element.document[1].document[0].title, "Macro is missing note")
            elif isinstance(doc, VariableDocumentation):
                self.assertIsInstance(element, Directive, "Wrong RST element generated for variable")
                self.assertEqual("data", element.document[0].title, "Wrong directive type for variable")
            elif isinstance(doc, GenericCommandDocumentation):
                self.assertIsInstance(element, Directive, "Wrong RST element generated for generic command")
                self.assertEqual("function", element.document[0].title, "Wrong directive type for generic command")
                self.assertEqual("warning", element.document[1].document[0].title, "Generic command is missing warning")
            elif isinstance(doc, ClassDocumentation):
                self.assertIsInstance(element, Directive, "Wrong RST element generated for class")
                self.assertEqual("py:class", element.document[0].title, "Wrong directive type for class")
            elif isinstance(doc, TestDocumentation):
                self.assertIsInstance(element, Directive, "Wrong RST element generated for test")
                self.assertEqual("function", element.document[0].title, "Wrong directive type for test")
            elif isinstance(doc, SectionDocumentation):
                self.assertIsInstance(element, Directive, "Wrong RST element generated for test section")
                self.assertEqual("function", element.document[0].title, "Wrong directive type for test section")
            elif isinstance(doc, CTestDocumentation):
                self.assertIsInstance(element, Directive, "Wrong RST element generated for CTest test")
                self.assertEqual("function", element.document[0].title, "Wrong directive type for CTest test")
            else:
                self.fail(f"Unknown documentation type: {doc}")

    def test_incorrect_variable_type(self):
        var_doc = VariableDocumentation("name", "Not a valid variable type", "0", "This should fail")
        self.assertRaises(ValueError, var_doc.process,
                          RSTWriter("test_writer"))


if __name__ == '__main__':
    unittest.main()
