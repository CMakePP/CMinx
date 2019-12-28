#!/usr/bin/python3
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
    def __init__(self, files, output):
        self.output = output
        self.writer = RSTWriter(f"{files[0]}")
        #We need a string stream of some kind, FileStream is easiest
        self.input_stream = FileStream(files[0])

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
        #All of the documented commands are now stored in aggregator.documented,
        #each element is a namedtuple repesenting the type of documentation it is.
        #So far we can document functions, macros, and variables (only strings and lists built using set)
        self.process_docs(self.aggregator.documented)
        if self.output is not None:
             self.writer.write_to_file(self.output)
        else:
             print(self.writer)

    def process_docs(self, docs):
        for doc in docs:
            if isinstance(doc, FunctionDocumentation):
                self.process_function_doc(doc)
            elif isinstance(doc, MacroDocumentation):
                self.process_macro_doc(doc)
            elif isinstance(doc, VariableDocumentation):
                self.process_variable_doc(doc)


    def process_function_doc(self, doc):
        d = self.writer.directive("function", f"{doc.function}({' '.join(doc.params)})")
        d.text(doc.doc)

    def process_macro_doc(self, doc):
        d = self.writer.directive("function", f"{doc.macro}({' '.join(doc.params)})")
        warning = d.directive("warning", "This is a macro, and so does not introduce a new scope.")
        d.text(doc.doc)

    def process_variable_doc(self, doc):
        d = self.writer.directive("data", f"{doc.varname}")
        d.text(doc.doc)
        d.field("Default value", doc.value)
        d.field("type", doc.type)
