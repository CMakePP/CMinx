#################
Types of Comments
#################

According to CMinx, the content of a CMake file can be broken into three
categories:

#. Documentation comments - what CMinx extracts

#. Annotation comments - Comments, but should not be extracted by CMinx

#. CMake source code - Everything else

To distinguish between the documentation and annotation comments CMinx borrows
the convention that documentation comments start with an additional comment
character. Thus to indicate that a CMake comment is documentation use
:code:`#[[[` (the block comment should still end with :code:`#]]`). For example:

.. literalinclude:: ../../../tests/examples/example.cmake
   :language: cmake
   :lines: 7-20

For comparison, an annotation comment looks like:

.. literalinclude:: ../../../tests/examples/example.cmake
   :language: cmake
   :lines: 1-5
