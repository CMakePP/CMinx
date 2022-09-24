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
Documenting a CTest Test
############################

CMinx can be used to document a CTest test created by the
`add_test() <https://cmake.org/cmake/help/latest/command/add_test.html>`_ command.
Again, this is done analogous to other documentation use cases, *i.e.*, by
proceeding the ``add_test()`` command with a
documentation comment. For example,

.. literalinclude:: ../../../tests/test_samples/ctest_add_test.cmake
   :language: cmake

which generates:

.. literalinclude:: ../../../tests/test_samples/corr_rst/ctest_add_test.rst
   :language: rst
