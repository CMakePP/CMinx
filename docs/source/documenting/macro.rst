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
###################
Documenting a Macro
###################

From the perspective of a CMinx user, one documents a macro in the same manner
as a function. For example:

.. literalinclude:: ../../../tests/test_samples/basic_macro.cmake
   :language: cmake

Since macros and functions behave differently in CMake (the biggest difference
being that functions introduce a new scope, whereas macros do not). CMinx will
automatically note in the generated documentation whether the command being
documented is a function or a macro.

.. literalinclude:: ../../../tests/test_samples/corr_rst/basic_macro.rst
   :language: rst


CMinx supports the same documentation features for macros as it
does for :doc:`functions <./function>`. This includes determining
when a macro has keyword arguments as in the following example.

.. literalinclude:: ../../../tests/test_samples/advanced_macro.cmake
   :language: cmake

CMinx will automatically add :code:`**kwargs` to the macro signature line
in the output RST.

.. literalinclude:: ../../../tests/test_samples/corr_rst/advanced_macro.rst
   :language: rst