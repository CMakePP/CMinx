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
------------
CMinx API
------------

This is a list of all functions within the CMinx project. These functions are
meant for use by developers. Users should run the :code:`cminx` command.

Python Modules
^^^^^^^^^^^^^^

.. autosummary::
   :toctree: .autosummary


   cminx.rstwriter
   cminx.documenter
   cminx.aggregator
   cminx.parser.CMakeLexer
   cminx.parser.CMakeParser
   cminx.parser.CMakeListener
   cminx.parser.CMakeVisitor

Functions
^^^^^^^^^

.. autosummary::
   :toctree: .autosummary

   cminx.document
   cminx.document_single_file
   cminx.main

CMake Modules
^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 2

   cmake/index
