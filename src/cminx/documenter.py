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

from antlr4 import *

from cminx import Settings
from .parser import ParserErrorListener
from .parser.CMakeLexer import CMakeLexer
from .parser.CMakeParser import CMakeParser
from .parser.aggregator import DocumentationAggregator, MethodDocumentation, VarType
from .parser.aggregator import FunctionDocumentation, MacroDocumentation, VariableDocumentation, TestDocumentation, \
    SectionDocumentation, GenericCommandDocumentation, ClassDocumentation, AttributeDocumentation
from .rstwriter import Directive, RSTWriter


class Documenter(object):
    """
    Generates RST documentation from aggregated documentation, combining parser.aggregator and rstwriter.
    """

    def __init__(
            self,
            file: str,
            title: str = None,
            module_name: str = None,
            settings: Settings = Settings()):
        """
        :param file: CMake file to read documentation from.
        :param title: RST header title to use in the generated document.
        :param settings: Dictionary containing application settings for documentation
        """

        self.settings = settings

        title = file if title is None else title

        if module_name is None:
            module_name = title

        self.writer = RSTWriter(title, settings=settings)

        self.module = self.writer.directive("module", module_name)

        # We need a string stream of some kind, FileStream is easiest
        self.input_stream = FileStream(file)

        # Convert those strings into tokens and build a stream from those
        self.lexer = CMakeLexer(self.input_stream)
        self.stream = CommonTokenStream(self.lexer)

        # We now have a stream of CommonToken instead of strings, parsers
        # require this type of stream
        self.parser = CMakeParser(self.stream)
        self.parser.addErrorListener(ParserErrorListener())
        self.tree = self.parser.cmake_file()

        # Hard part is done, we now have a fully usable parse tree, now we just
        # need to walk it
        self.aggregator = DocumentationAggregator(settings)
        self.walker = ParseTreeWalker()
        self.walker.walk(self.aggregator, self.tree)

    def process(self):
        """
        Process Documenter.aggregator.documented and build RST document from it.

        :return: Completed RSTWriter document, also located in Documenter.writer
        """

        # All of the documented commands are now stored in aggregator.documented,
        # each element is a namedtuple repesenting the type of documentation it is.
        # So far we can document functions, macros, and variables (only strings
        # and lists built using set)
        self.process_docs(self.aggregator.documented)
        return self.writer

    def process_docs(self, docs):
        """
        Loops over document and dispatches each documentation to the respective processor.

        :param docs: List of documentation objects.
        """

        for doc in docs:
            # Dispatch doc to correct processor
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
            elif isinstance(doc, GenericCommandDocumentation):
                self.process_generic_command_doc(doc)
            else:
                raise ValueError(
                    f"Unknown documentation type {str(type(doc))}: {str(doc)}")

    def process_function_doc(self, doc: FunctionDocumentation):
        """
        FunctionDocumentation processor. Generates the RST "function" directive.

        :param doc: Documentation for the function
        :type doc: FunctionDocumentation
        """

        d = self.writer.directive(
            "function", f"{doc.function}({' '.join(doc.params)})")
        d.text(doc.doc)

    def process_macro_doc(self, doc):
        """
        MacroDocumentation processor. Generates the RST "function" directive containing
        a "warning" directive explaining that it is a macro.

        :param doc: Documentation for the macro
        :type doc: MacroDocumentation
        """

        d = self.writer.directive(
            "function", f"{doc.macro}({' '.join(doc.params)})")
        warning = d.directive(
            "warning",
            "This is a macro, and so does not introduce a new scope.")
        d.text(doc.doc)

    def process_test_doc(self, doc):
        """
        TestDocumentation processor. Generates the RST "function" directive containing
        a "warning" directive explaining that it is a test.

        :param doc: Documentation for the test
        :type doc: TestDocumentation
        """

        d = self.writer.directive(
            "function",
            f"{doc.name}({'EXPECTFAIL' if doc.expect_fail else ''})")
        warning = d.directive(
            "warning",
            "This is a CMakeTest test definition, do not call this manually.")
        d.text(doc.doc)

    def process_section_doc(self, doc):
        """
        SectionDocumentation processor. Generates the RST "function" directive containing
        a "warning" directive explaining that it is a test.

        :param doc: Documentation for the test
        :type doc: SectionDocumentation
        """

        d = self.writer.directive(
            "function",
            f"{doc.name}({'EXPECTFAIL' if doc.expect_fail else ''})")
        warning = d.directive(
            "warning",
            "This is a CMakeTest section definition, do not call this manually.")
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
        if doc.type == VarType.String:
            var_type = "str"
        elif doc.type == VarType.List:
            var_type = "list"
        elif doc.type == VarType.Unset:
            var_type = "UNSET"
        else:
            raise ValueError("Unknown variable type: " + doc.type)
        d.field("type", var_type)

    def process_generic_command_doc(self, doc):
        """
        This method processes any documented commands that don't have any other processors.
        All it does is generate a function directive containing the command's name and arguments,
        and adds a warning that it's just an invocation and not a definition.
        """
        d = self.writer.directive(
            "function", f"{doc.name}({' '.join(doc.params)})")
        warning = d.directive(
            "warning",
            "This is a generic command invocation. It is not a function or macro definition.")
        d.text(doc.doc)

    def process_class_doc(self, doc: ClassDocumentation):
        """
        Adds a py:class directive containing information on the CMakePP
        class that was documented, including all attributes, constructors, and members
        """

        d = self.writer.directive("py:class", f"{doc.name}")
        if len(doc.superclasses) > 0:
            bases = "Bases: " + \
                    ", ".join(
                        f":class:`{superclass}`" for superclass in doc.superclasses)
            d.text(bases + '\n')
        d.text(doc.doc)

        if len(doc.members) > 0:
            d.text("**Additional Constructors**")

        for member in doc.constructors:
            self.add_method_doc(member, d)

        if len(doc.members) > 0:
            d.text("**Methods**")

        for member in doc.members:
            self.add_method_doc(member, d)

        if len(doc.attributes) > 0:
            d.text("**Attributes**")

        for attribute in doc.attributes:
            self.add_attr_doc(attribute, d)

    def add_method_doc(
            self,
            doc: MethodDocumentation,
            class_directive: Directive):
        """
        Adds a py:method directive to the supplied class directive
        using the supplied MethodDocumentation to determine whether
        the member is a constructor or not, as well as what params and
        types the member has.
        """
        params_pretty = ', '.join(
            doc.params) + ("[, ...]" if "args" in doc.param_types else "")
        d = class_directive.directive(
            "py:method", f"{doc.name}({params_pretty})")
        if doc.is_macro:
            d.directive(
                "note",
                "This member is a macro and so does not introduce a new scope")
        # if doc.is_constructor:
        #     info = d.directive("admonition", "info")
        #     info.text("This member is a constructor.")
        d.text(doc.doc)
        for i in range(len(doc.param_types)):
            if i >= len(doc.params):
                break
            if f":param {doc.params[i]}:" not in doc.doc:
                d.field(f"param {doc.params[i]}", "")
            if f":type {doc.params[i]}:" not in doc.doc:
                d.field(f"type {doc.params[i]}", doc.param_types[i])

    def add_attr_doc(
            self,
            doc: AttributeDocumentation,
            class_directive: Directive):
        """
        Creates and adds a py:attribute directive to the supplied class directive.
        """
        d = class_directive.directive("py:attribute", f"{doc.name}")
        if doc.default_value is not None:
            d.option("value", doc.default_value)

        d.text(doc.doc)
