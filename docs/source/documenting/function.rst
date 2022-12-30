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

The following sections describe the aspects of this template in more detail.

Basic Function Documentation
============================

As an example consider the very simple CMake function ``say_hi_to`` defined as:

.. literalinclude:: ../../../tests/test_samples/basic_function.cmake
   :language: cmake
   :lines: 12-14

``say_hi_to`` takes one positional argument ``person`` which is the name of the
person we want to say hi to.  For documenting positional arguments it is
recommended you use the ``:param:`` field like:

.. literalinclude:: ../../../tests/test_samples/basic_function.cmake
   :language: cmake
   :lines: 3-14

Running CMinx on the documented code will generate:

.. literalinclude:: ../../../tests/test_samples/corr_rst/basic_function.rst
   :language: rst
   :lines: 9-17

.. note::

   Since CMake is an interpreted language, it may not be obvious at first, but
   CMake does have types. In one context or another, native CMake distinguishes
   among: booleans, command names, file paths, floating-point numbers, integers,
   generator expressions, target names, strings, and lists. A list can contain
   any of the aforementioned types (including other lists) and all objects can
   be implicitly converted to stings.

The documentation comment has three parts:

.. literalinclude:: ../../../tests/test_samples/basic_function.cmake
   :lines: 4
   :language: none

is the short/brief description; it's used to quickly summarize what the function
does. The short description is often used when a user is trying to quickly
ascertain what functionality a CMake module provides.

.. literalinclude:: ../../../tests/test_samples/basic_function.cmake
   :lines: 6-7
   :language: none

is the detailed description; it's used to provide more in depth documentation
beyond the brief description. Finally,

.. literalinclude:: ../../../tests/test_samples/basic_function.cmake
   :lines: 9-10
   :language: none

documents the positional arguments to the function including how they are used
and what their types.

Documenting Keyword Arguments
=============================

In modern CMake it is common practice for functions that accept many
arguments, to accept those arguments as keyword arguments instead of
positional arguments. As an example consider an "advanced" version of
``say_hi_to`` defined as:

.. literalinclude:: ../../../tests/test_samples/advanced_function.cmake
   :language: cmake
   :lines: 18-22

Although not strictly necessary, most CMake function implementations handle
keyword arguments by calling ``cmake_parse_arguments``. The arguments to
``cmake_parse_arguments`` are the keywords the function recognizes; in this
example the keyword arguments are ``PERSONS`` and ``CATS`` (see
`here <https://cmake.org/cmake/help/latest/command/cmake_parse_arguments.html>`__
for more details about ``cmake_parse_arguments``).

Documenting keyword arguments is similar to documenting positional parameters
except that instead of using the ``:param:`` field, one uses ``:keyword:``:

.. literalinclude:: ../../../tests/test_samples/advanced_function.cmake
   :language: cmake
   :lines: 1-22

Running CMinx on this code generates:

.. literalinclude:: ../../../tests/test_samples/corr_rst/advanced_function.rst
   :language: rst
   :lines: 9-25

Notice how the function signature was automatically
updated to include a ``**kwargs`` parameter. CMinx will do
this for any function that calls ``cmake_parse_arguments`` or
includes ``:keyword`` in its doc comment, the latter of which
is configurable. If this is not desired, it can be turned
off through the configuration file.

.. note::

   While it is recommended that you document positional arguments differently
   than keyword arguments by using ``:param:`` vs. ``:keyword:`` the resulting
   HTML documentation may end up rendering the two the same. Thus, one should
   place a separator to clearly define which are keyword arguments.

CMake arguments can not only be keywords, where a value is supplied after the keyword,
but can also be switches or options, where the keyword itself toggles the option and
no subsequent value is passed. For these arguments, document them as part of the
keyword arguments but set the type as ``option``.

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
