##############################
Overview of How CMakeDoc Works
##############################

-------
Parsing
-------

.. sidebar:: Source File Parsing.

   .. _parsing_flowchart:
   .. figure:: uml_diagrams/parsing.png

      How CMakeDoc parses a CMake source file.

In CMakeDoc parsing of a source file is the role of the Antlr4 parsing runtime, generated from
the modified CMake.g4 grammar file.

#. As per the standard usage, the file contents are read into an
   Antlr4 FileStream, which is then passed to the generated CMake lexer.
#. The lexer generates a token stream, which is then fed into the CMakeParser.
#. The parser generates a tree of parse elements, called contexts,
   which are then walked over by the ParseTreeWalker.
#. The walker calls the aggregator methods upon entering or exiting
   parse rules, such as entering a DocumentedCommand parse rule.
#. The documentation aggregator generates NamedTuples representing the type
   of documentation generated, such as FunctionDocumentation, complete
   with all relevant information, and adds them to a *documented* list.
#. From there, Documenter loops over the documentation list,
   generating equivalent RST via RSTWriter for each type of documentation.

This process is diagrammatically summarized in :numref:`parsing_flowchart`.
