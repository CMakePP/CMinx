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
   config
   documenting/index
   full_example
   usage
   about
   developer/index
