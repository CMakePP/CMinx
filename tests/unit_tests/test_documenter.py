#!/usr/bin/python3
import context
import unittest
import sys
import docutils
from cminx.rstwriter import Directive
from cminx.parser.aggregator import FunctionDocumentation, MacroDocumentation, VariableDocumentation
from cminx.documenter import Documenter
from rst_validator import RSTValidator


class TestDocumenter(unittest.TestCase):

    def setUp(self):
        self.filename = context.example_cmake
        self.reset()

    def reset(self):
       self.documenter = Documenter(self.filename, self.filename) #File is parsed on __init__

    def test_process(self):
       self.documenter.process()  #Convert all documentation into RST
       self.assertEqual(len(self.documenter.aggregator.documented), len(self.documenter.writer.document) - 2, "Generated RST has different length from input documentation") #RSTWriter adds one element for document heading, documenter adds another for module definition
       for i in range(0, len(self.documenter.aggregator.documented)):
            doc = self.documenter.aggregator.documented[i]
            element = self.documenter.writer.document[i + 2]
            if isinstance(doc, FunctionDocumentation):
                self.assertIsInstance(element, Directive, "Wrong RST element generated for function")
                self.assertEqual("function", element.document[0].title, "Wrong directive type for function")
            elif isinstance(doc, MacroDocumentation):
                self.assertIsInstance(element, Directive, "Wrong RST element generated for macro")
                self.assertEqual("function", element.document[0].title, "Wrong directive type for macro")
                self.assertIsInstance(element.document[1], Directive)
                self.assertEqual("warning", element.document[1].document[0].title, "Macro is missing warning")
            elif isinstance(doc, VariableDocumentation):
                self.assertIsInstance(element, Directive, "Wrong RST element generated for variable")
                self.assertEqual("data", element.document[0].title, "Wrong directive type for variable")


if __name__ == '__main__':
    unittest.main()
