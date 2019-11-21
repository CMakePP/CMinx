#!/usr/bin/python3

import sys
from antlr4 import *
from cmakedoc.parser.CMakeLexer import CMakeLexer
from cmakedoc.parser.CMakeParser import CMakeParser
from cmakedoc.parser.CMakeListener import CMakeListener
from cmakedoc.parser.aggregator import DocumentationAggregator


def main(argv):
    #We need a string stream of some kind, FileStream is easiest
    input_stream = FileStream(argv[1])

    #Convert those strings into tokens and build a stream from those
    lexer = CMakeLexer(input_stream)
    stream = CommonTokenStream(lexer)

    #We now have a stream of CommonToken instead of strings, parsers require this type of stream
    parser = CMakeParser(stream)
    tree = parser.cmake_file()

    #Hard part is done, we now have a fully useable parse tree, now we just need to walk it
    aggregator = DocumentationAggregator()
    walker = ParseTreeWalker()
    walker.walk(aggregator, tree)

    #All of the documented commands are now stored in aggregator.documented,
    #each element is a namedtuple repesenting the type of documentation it is.
    #So far we can document functions, macros, and variables (only strings and lists built using set)
    print(aggregator.documented)

if __name__ == '__main__':
    #Usage: aggregator_example.py <file>.cmake
    main(sys.argv)
