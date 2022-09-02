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

import sys
from antlr4 import *
from cminx.parser.CMakeLexer import CMakeLexer
from cminx.parser.CMakeParser import CMakeParser
from aggregator import DocumentationAggregator


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
