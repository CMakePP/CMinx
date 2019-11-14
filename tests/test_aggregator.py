#!/usr/bin/python3
import context
import unittest
import sys
from antlr4 import *
from cmakedoc.parser.CMakeLexer import CMakeLexer
from cmakedoc.parser.CMakeParser import CMakeParser
from cmakedoc.parser.CMakeListener import CMakeListener
from cmakedoc.parser.aggregator import DocumentationAggregator


class TestAggregator(unittest.TestCase):

    def setUp(argv):
        self.filename = "test_samples/basic_function.cmake"
        #We need a string stream of some kind, FileStream is easiest
        self.input_stream = FileStream(self.filename)
        self.reset()

    def reset(self):
        #Convert those strings into tokens and build a stream from those
        self.lexer = CMakeLexer(self.input_stream)
        self.stream = CommonTokenStream(self.lexer)

        #We now have a stream of CommonToken instead of strings, parsers require this type of stream
        self.parser = CMakeParser(self.stream)
        self.tree = self.parser.cmake_file()

        #Hard part is done, we now have a fully useable parse tree, now we just need to walk it
        self.aggregator = DocumentationAggregator()
        self.walker = ParseTreeWalker()
        self.walker.walk(self.aggregator, self.tree)


    def test_aggregated_docs(self):

        #All of the documented commands are now stored in aggregator.documented,
        #each element is a namedtuple repesenting the type of documentation it is.
        #So far we can document functions, macros, and variables (only strings and lists built using set)
        print(aggregator.documented)

   def test_bad_syntax(self):
       self.input_stream = 

if __name__ == '__main__':
    #Usage: aggregator_example.py <file>.cmake
    main(sys.argv)
