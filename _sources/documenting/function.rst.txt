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
**********************
Documenting a Function
**********************

CMinx more or less copies your documentation comments verbatim to the resulting
reST file. Strictly speaking this means you can put whatever you want in the
comments; however, it is strongly recommended that you follow usual Python reST
conventions so that you can get the most out of Sphinx's parsing of the reST
file. A good template is:

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

Recommended reST Directives
===========================

reST's default set of directives encompasses many language nuances which are
not found in the CMake language. Of the default reST directives, the ones that
map directly to aspects of the CMake language are:

- ``:param <name of parameter>: <description of parameter>``
- ``:keyword <name of keyword>: <description of keyword>``
- ``:type <name of parameter>: <type of parameter named "name of parameter">``

Respectively these document: positional arguments, keyword arguments (*i.e.*,
arguments to be parsed by ``cmake_parse_arguments``), and the type of a
positional argument or keyword. Unlike most languages CMake does not natively
support returns.

.. note::

   Since CMake is an interpreted language, it may not be obvious at first, but
   CMake does have types. In one context or another, native CMake distinguishes
   among: booleans, command names, file paths, floating-point numbers, integers,
   generator expressions, target names, strings, and lists. A list can contain
   any of the aforementioned types (including other lists) and all objects can
   be implicitly converted to stings.

An example using all three of these directives:

.. literalinclude:: ../../../tests/test_samples/advanced_function.cmake
   :language: cmake

Assuming the above CMake lives in the file ``advanced_function.cmake``, CMinx
will generate the reST file:

.. literalinclude:: ../../../tests/test_samples/corr_rst/advanced_function.rst
   :language: rst
