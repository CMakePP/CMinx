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

Sometimes documentation comments need additional information in their
headers to inform CMinx about the type of documentation the comment
represents. This information is contained in the first
line of the documentation comment (the line with :code:`#[[[`)
and is marked by a special directive start character :code:`@`.
For example, a module documentation comment contains the :code:`@module`
directive:

.. literalinclude:: ../../../tests/test_samples/basic_module.cmake
   :language: cmake
   :lines: 1-9

.. note::
   Doccomment directives marked by :code:`@` are different from RST directives.
   They are hints to CMinx for how to parse the doccomment and how to format
   it in the output, they *are not* passed through to the generated RST
   and therefore Sphinx is entirely unaware of them. Consider them akin to
   preprocessor directives.

