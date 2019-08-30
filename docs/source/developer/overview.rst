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

In CMakeDoc parsing of a source file is the role of the ``Parser`` class. Given
a ``Parser`` instance:

#. The contents of a CMake source file are fed to the instance's ``parse``
   member function.
#. The ``parse`` function instance loops over the file's contents line-by-line.
#. For each line a ``CMakeRegexer`` instance identifies what the line does
   (*e.g.*, is it the start of a user-defined CMake function, a block comment,
   or a blank line).
#. Once the purpose of the line is known, ``parse`` dispatches the file buffer
   to an appropriate handler function.
#. The handler extracts the block of CMake code and advances the file buffer to
   past the extracted code.
#. ``parse`` repeats this process with the next line in the buffer until the
   file buffer is depleted.
#. ``parse`` returns a list of the code blocks, tagged with its purpose.

This process is diagrammatically summarized in :numref:`parsing_flowchart`.
