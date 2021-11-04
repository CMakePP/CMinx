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
############################
Documenting a CMakeTest Test
############################

CMinx can be used to document
`CMakeTest <https://github.com/CMakePP/CMakeTest>`_ tests and test sections.
Again, this is done analogous to other documentation use cases, *i.e.*, by
proceeding the ``ct_add_test`` or ``ct_add_section`` command with a
documentation comment. For example,

.. literalinclude:: ../../../tests/test_samples/ct_test.cmake
   :language: cmake

which generates:

.. literalinclude:: ../../../tests/test_samples/corr_rst/ct_test.rst
   :language: rst
