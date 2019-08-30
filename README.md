# CMakeDoc
[![Build Status](https://travis-ci.com/CMakePP/CMakeDoc.svg?branch=master)](
https://travis-ci.com/CMakePP/CMakeDoc)
[![codecov](
https://codecov.io/gh/CMakePP/CMakeDoc/branch/master/graph/badge.svg)](
https://codecov.io/gh/CMakePP/CMakeDoc)
[![Documentation Status](
https://readthedocs.org/projects/cmakedoc/badge/?version=latest)](
https://cmakedoc.readthedocs.io/en/latest/?badge=latest)

A common software practice is to keep documentation close to the functions and
classes that are being documented (ideally in the same source file). Most
languages have mechanisms for doing this for example Python has docstrings and
C++ has Doxygen. To our knowledge no such solution exists for CMake. CMakeDoc
fixes this.

CMakeDoc is a Python package that extracts documentation from CMake source
files. CMake developers document their functions by immediately proceeding the
function with a comment block written in reStructuredText (reST). CMakeDoc will
extract the comment blocks verbatim and create `*.rst` files which can be
included in a normal Sphinx documentation set-up.
