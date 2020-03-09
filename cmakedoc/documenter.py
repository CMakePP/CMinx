
"""
This file contains the Documenter class, which combines functionality
from parser.aggregator and rstwriter to generate RST documentation
for CMake files.

:Author: Branden Butler
:License: Apache 2.0

"""



import sys
from antlr4 import *
from .parser import ParserErrorListener
from .parser.CMakeLexer import CMakeLexer
from .parser.CMakeParser import CMakeParser
from .parser.CMakeListener import CMakeListener
from .rstwriter import RSTWriter
from .parser.aggregator import DocumentationAggregator
from .parser.aggregator import FunctionDocumentation, MacroDocumentation, VariableDocumentation



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
