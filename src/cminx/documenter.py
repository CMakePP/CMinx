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
This file contains the Documenter class, which is the top-level
entrypoint into the CMinx documentation system. It handles parsing,
aggregating, and RST writing.

:Author: Branden Butler
:License: Apache 2.0

"""
from typing import List

from antlr4 import *

from .aggregator import DocumentationAggregator
from cminx import Settings
from .documentation_types import DocumentationType, ModuleDocumentation
from .parser import ParserErrorListener
from .parser.CMakeLexer import CMakeLexer
from .parser.CMakeParser import CMakeParser
from .rstwriter import RSTWriter, Directive


class Documenter(object):
    """
    Generates RST documentation from aggregated documentation, combining
    :class:`~cminx.aggregator.DocumentationAggregator` and :class:`~cminx.rstwriter.RSTWriter`.
    The entrypoint for this class is the :meth:`process` method.
    """

    def __init__(
            self,
            file: str,
            title: str = None,
            module_name: str = None,
            settings: Settings = Settings()) -> None:
        """
        :param file: CMake file to read documentation from.
        :param title: RST header title to use in the generated document.
        :param module_name: The name of the CMake module, used in the module directive if
                            no other name is given in a module doccomment.
        :param settings: Dictionary containing application settings for documentation
        """

        self.settings: Settings = settings
        """Settings used for aggregation and RST generation, passed down to all downstream components."""

        title = file if title is None else title

        if module_name is None:
            module_name = title

        self.module_name: str = module_name
        """The name of the CMake module, used as a default when no name given via a module doccomment."""

        self.writer: RSTWriter = RSTWriter(title, settings=settings)
        """The writer that is passed to the aggregated documentation objects."""

        self.module: Directive
        """The :code:`.. module::` directive that defines the module's name."""

        # We need a string stream of some kind, FileStream is easiest
        self.input_stream: InputStream = FileStream(file)
        """The string stream used to read the CMake file."""

        # Convert those strings into tokens and build a stream from those
        self.lexer: CMakeLexer = CMakeLexer(self.input_stream)
        """The lexer used to generate the token stream."""

        self.stream: TokenStream = CommonTokenStream(self.lexer)
        """The stream of tokens from the lexer, should be passed to the parser."""

        # We now have a stream of CommonToken instead of strings, parsers
        # require this type of stream
        self.parser: CMakeParser = CMakeParser(self.stream)
        """
        The parser used to parse the token stream and call our listener.
        By default, an instance of :class:`~cminx.parser.ParserErrorListener` is
        added.
        """

        self.parser.addErrorListener(ParserErrorListener())

        # Hard part is done, we now have a fully usable parse tree, now we just
        # need to walk it
        self.aggregator: DocumentationAggregator = DocumentationAggregator(settings)
        """The aggregator used to listen for parser rules and generate documentation objects."""

        self.walker: ParseTreeWalker = ParseTreeWalker()
        """Walks the parser tree at a given parser rule, used to kick off aggregation."""

    def process(self) -> RSTWriter:
        """
        Process :attr:`cminx.aggregator.DocumentationAggregator.documented` and build RST document from it.

        :return: Completed RSTWriter document, also located in :attr:`Documenter.writer`
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

    def process_docs(self, docs: List[DocumentationType]) -> None:
        """
        Loops over document and calls :meth:`cminx.documentation_types.DocumentationType.process` with
        :attr:`~Documenter.writer`.

        :param docs: List of documentation objects.
        """

        module_docs = [x for x in docs if isinstance(x, ModuleDocumentation)]

        if len(module_docs) == 0:
            docs.insert(0, ModuleDocumentation(self.module_name, ""))

        for module_doc in module_docs:
            if module_doc.name is None or len(module_doc.name) == 0:
                module_doc.name = self.module_name
            else:
                self.writer.title = module_doc.name

        for doc in docs:
            doc.process(self.writer)
