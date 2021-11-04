.. Copyright 2021 CMakePP
..
.. Licensed under the Apache License, Version 2.0 (the "License");
.. you may not use this file except in compliance with the License.
.. You may obtain a copy of the License at
..
.. http://www.apache.org/licenses/LICENSE-2.0
..
.. Unless required by applicable law or agreed to in writing, software
.. distributed under the License is distributed on an "AS IS" BASIS,
.. WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
.. See the License for the specific language governing permissions and
.. limitations under the License.
..
##############################
Overview of How CMinx Works
##############################

.. sidebar:: Source File Parsing

   .. _parsing_flowchart:
   .. figure:: uml_diagrams/parsing.png

      How CMinx parses a CMake source file.


   .. _aggregation_flowchart:
   .. figure:: uml_diagrams/aggregation.png

      How CMinx aggregates documentation from the parse tree.

-------
Parsing
-------



In CMinx parsing of a source file is the role of the Antlr4 parsing runtime, generated from
the modified CMake.g4 grammar file.

#. As per the standard usage, the file contents are read into an
   Antlr4 FileStream, which is then passed to the generated CMake lexer.
#. The lexer generates a token stream, which is then fed into the CMakeParser.
#. The parser generates a tree of parse elements, called contexts,
   which are then walked over by the ParseTreeWalker.

This process is diagrammatically summarized in :numref:`parsing_flowchart`.


-----------
Aggregation
-----------

After the parser generates the parse tree, CMinx walks the tree and aggregates the various documentation.

#. The walker calls the aggregator methods upon entering or exiting
   parse rules, such as entering a :code:`documented_command` parse rule.
#. The parse rule enterDocumented_command cleans the doccomment and
   extracts the documented command. For example, if a function definition
   is documented, enterDocumented_command will extract the :code:`function` command.
#. The aggregator then locates the subprocessor that corresponds to the extracted command,
   for example if the extracted command is :code:`function` then the subprocessor would be
   :code:`process_function()`. This subhandler is then executed with the parse context and
   cleaned docstring.
#. The documentation aggregator subhandler generates NamedTuples representing the type
   of documentation generated, such as FunctionDocumentation, complete
   with all relevant information, and adds them to a *documented* list.
#. From there, Documenter loops over the documentation list,
   generating equivalent RST via RSTWriter for each type of documentation.

This process is diagrammatically summarized in :numref:`aggregation_flowchart`.
