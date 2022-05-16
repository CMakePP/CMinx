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
"""
This file contains the Documenter class, which combines functionality
from parser.aggregator and rstwriter to generate RST documentation
for CMake files.

:Author: Branden Butler
:License: Apache 2.0

"""



from audioop import add
import sys
from antlr4 import *
from pytest import param
from .parser import ParserErrorListener
from .parser.CMakeLexer import CMakeLexer
from .parser.CMakeParser import CMakeParser
from .parser.CMakeListener import CMakeListener
from .rstwriter import Directive, RSTWriter
from .parser.aggregator import DocumentationAggregator, MethodDocumentation
from .parser.aggregator import FunctionDocumentation, MacroDocumentation, VariableDocumentation, TestDocumentation, SectionDocumentation, GenericCommandDocumentation, ClassDocumentation, AttributeDocumentation



class Documenter(object):
    """
    Generates RST documentation from aggregated documentation, combining parser.aggregator and rstwriter.
    """

    def __init__(self, file: str, title: str = None):
        """
        :param file: CMake file to read documentation from.
        :param title: RST header title to use in the generated document.
        """

        title =  file if title is None else title

        self.writer = RSTWriter(title)

        self.module = self.writer.directive("module", title)

        self.classes = {}

        #We need a string stream of some kind, FileStream is easiest
        self.input_stream = FileStream(file)

        #Convert those strings into tokens and build a stream from those
        self.lexer = CMakeLexer(self.input_stream)
        self.stream = CommonTokenStream(self.lexer)

        #We now have a stream of CommonToken instead of strings, parsers require this type of stream
        self.parser = CMakeParser(self.stream)
        self.parser.addErrorListener(ParserErrorListener())
        self.tree = self.parser.cmake_file()

        #Hard part is done, we now have a fully useable parse tree, now we just need to walk it
        self.aggregator = DocumentationAggregator()
        self.walker = ParseTreeWalker()
        self.walker.walk(self.aggregator, self.tree)


    def process(self):
        """
        Process Documenter.aggregator.documented and build RST document from it.

        :return: Completed RSTWriter document, also located in Documenter.writer
        """

        #All of the documented commands are now stored in aggregator.documented,
        #each element is a namedtuple repesenting the type of documentation it is.
        #So far we can document functions, macros, and variables (only strings and lists built using set)
        self.process_docs(self.aggregator.documented)
        return self.writer

    def process_docs(self, docs):
        """
        Loops over document and dispatches each documentation to the respective processor.

        :param docs: List of documentation objects.
        """

        for doc in docs:
            #Dispatch doc to correct processor
            if isinstance(doc, FunctionDocumentation):
                self.process_function_doc(doc)
            elif isinstance(doc, MacroDocumentation):
                self.process_macro_doc(doc)
            elif isinstance(doc, VariableDocumentation):
                self.process_variable_doc(doc)
            elif isinstance(doc, TestDocumentation):
                self.process_test_doc(doc)
            elif isinstance(doc, SectionDocumentation):
                self.process_section_doc(doc)
            elif isinstance(doc, ClassDocumentation):
                self.process_class_doc(doc)
            elif isinstance(doc, AttributeDocumentation):
                self.process_attr_doc(doc)
            elif isinstance(doc, GenericCommandDocumentation):
                self.process_generic_command_doc(doc)
            else:
                raise ValueError(f"Unknown documentation type {str(type(doc))}: {str(doc)}")


    def process_function_doc(self, doc: FunctionDocumentation):
        """
        FunctionDocumentation processor. Generates the RST "function" directive.

        :param doc: Documentation for the function
        :type doc: FunctionDocumentation
        """

        d = self.writer.directive("function", f"{doc.function}({' '.join(doc.params)})")
        d.text(doc.doc)

    def process_macro_doc(self, doc):
        """
        MacroDocumentation processor. Generates the RST "function" directive containing
        a "warning" directive explaining that it is a macro.

        :param doc: Documentation for the macro
        :type doc: MacroDocumentation
        """

        d = self.writer.directive("function", f"{doc.macro}({' '.join(doc.params)})")
        warning = d.directive("warning", "This is a macro, and so does not introduce a new scope.")
        d.text(doc.doc)

    def process_test_doc(self, doc):
        """
        TestDocumentation processor. Generates the RST "function" directive containing
        a "warning" directive explaining that it is a test.

        :param doc: Documentation for the test
        :type doc: TestDocumentation
        """

        d = self.writer.directive("function", f"{doc.name}({'EXPECTFAIL' if doc.expect_fail else ''})")
        warning = d.directive("warning", "This is a CMakeTest test definition, do not call this manually.")
        d.text(doc.doc)

    def process_section_doc(self, doc):
        """
        SectionDocumentation processor. Generates the RST "function" directive containing
        a "warning" directive explaining that it is a test.

        :param doc: Documentation for the test
        :type doc: SectionDocumentation
        """

        d = self.writer.directive("function", f"{doc.name}({'EXPECTFAIL' if doc.expect_fail else ''})")
        warning = d.directive("warning", "This is a CMakeTest section definition, do not call this manually.")
        d.text(doc.doc)

    def process_variable_doc(self, doc):
        """
        VariableDocumentation processor. Generates the RST "data" directive.

        :param doc: Documentation for the variable.
        :type doc: VariableDocumentation
        """

        d = self.writer.directive("data", f"{doc.varname}")
        d.text(doc.doc)
        d.field("Default value", doc.value)
        d.field("type", doc.type)


    def process_generic_command_doc(self, doc):
        d = self.writer.directive("function", f"{doc.name}({' '.join(doc.params)})")
        warning = d.directive("warning", "This is a generic command invocation. It is not a function or macro definition.")
        d.text(doc.doc)

    def process_class_doc(self, doc: ClassDocumentation):
        d = self.writer.directive("py:class", f"{doc.name}({' '.join(doc.superclasses)})")
        d.text(doc.doc)

        for member in doc.members:
            if isinstance(member, AttributeDocumentation):
                self.add_attr_doc(member, d)
            elif isinstance(member, MethodDocumentation):
                self.add_method_doc(member, d)
            else:
                raise ValueError(f"Unknown member documentation type {str(type(member))}: {str(member)}")

    def add_method_doc(self, doc: MethodDocumentation, class_directive: Directive):
        params_pretty = ', '.join(doc.params) + "[, ...]" if "args" in doc.param_types else ""
        d = class_directive.directive("py:method", f"{doc.name}({params_pretty})")
        d.text(doc.doc)
        for i in range(len(doc.param_types)):
            if i >= len(doc.params):
                break
            if f":param {doc.params[i]}:" not in doc.doc:
                d.field(f"param {doc.params[i]}", "")
            if f":type {doc.params[i]}:" not in doc.doc:
                d.field(f"type {doc.params[i]}", doc.param_types[i])

    def add_attr_doc(self, doc: AttributeDocumentation, class_directive: Directive):
        d = class_directive.directive("py:attribute", f"{doc.name}")
        if doc.default_value is not None:
            d.option("value", doc.default_value)

        d.text(doc.doc)
