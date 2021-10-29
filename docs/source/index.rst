#####
CMinx
#####

A common software practice is to keep documentation close to the functions and
classes that are being documented (ideally in the same source file). Most
languages have established mechanisms for doing this, for example Python has
docstrings and C++ has Doxygen. To our knowledge no such solution exists for
CMake. CMinx fixes this.

CMinx is modeled after Python's docstrings. CMake developers document their
functions with comment blocks written in reStructuredText (reST). CMinx will
then extract the comment blocks and create `*.rst` files which can be included
in a normal Sphinx documentation set-up.

*****************
Table Of Contents
*****************

.. toctree::
   :maxdepth: 2

   installation
   quickstart
   documenting/index
   full_example
   usage
   about
   developer/index
