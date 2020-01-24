----------
Quickstart
----------

.. note::

   This tutorial assumes you are familiar with reStructuredText (reST) and
   CMake.

According to CMakeDoc, the contents of a CMake file can be broken into three
categories:

#. Documentation comments - what CMakeDoc extracts

#. Annotation comments - Comments that are not documentation

#. CMake source code - Everything else

To distinguish between the two types of comments CMakeDoc borrows the convention
that documentation comments start with an additional comment character. Thus to
indicate that a CMake comment is documentation use ``#[[[`` (the block
comment should still end with ``#]]``).

The contents of the documentation comments should follow usual Python reST
conventions. In other words:

.. code:: cmake

   #[[[ 
   # Short description. Runs up to the first blank line. So this is still the
   # short description.
   #
   # Longer description goes here and includes all text and paragraphs from
   # here forward that are not part of reST directives.
   #
   # The parameters, keywords, and their types will be pulled out of the longer
   # description and placed in separate sections regardless of where they
   # appear.
   #
   # :param name_of_param: Description of what `name_of_param` is used for
   #
   # The next line is a reST directive and will not be part of the longer
   # description.
   #
   # .. note::
   #
   #    This is a note, it will show up using reST's native note section
   #]]

Technically speaking the contents of the comments are dumped more-or-less
verbatim into the resulting ``*.rst`` file so you can use any reST directives
and markup you like. That said, you will probably only want to use:

- ``:param <name of parameter>: <description of parameter>``
- ``:type <name of parameter>: <type of parameter named "name of parameter">``
- ``:keyword <name of keyword>: <description of keyword>``

as those are the subset of Python language features CMake actually supports.
