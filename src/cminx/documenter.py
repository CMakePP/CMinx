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
from typing import List

from antlr4 import *

from .aggregator import DocumentationAggregator
from cminx import Settings
from .documentation_types import DocumentationType
from .parser import ParserErrorListener
from .parser.CMakeLexer import CMakeLexer
from .parser.CMakeParser import CMakeParser
from .rstwriter import RSTWriter


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

        # Hard part is done, we now have a fully usable parse tree, now we just
        # need to walk it
        self.aggregator = DocumentationAggregator(settings)
        self.walker = ParseTreeWalker()

    def process(self) -> RSTWriter:
        """
        Process Documenter.aggregator.documented and build RST document from it.

        :return: Completed RSTWriter document, also located in Documenter.writer
        """

        # Parse and lex the file, then walk the tree and aggregate the
        # documented commands
        self.walker.walk(self.aggregator, self.parser.cmake_file())

        # All the documented commands are now stored in aggregator.documented,
        # each element is a namedtuple representing the type of documentation it is.
        # So far we can document functions, macros, and variables (only strings
        # and lists built using set)
        self.process_docs(self.aggregator.documented)
        return self.writer

    def process_docs(self, docs: List[DocumentationType]):
        """
        Loops over document and calls Documentation.process() with self.writer

        :param docs: List of documentation objects.
        """

        for doc in docs:
            doc.process(self.writer)
