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
Documenting CMinx
#################

This page contains notes for developers on how to update the CMinx
documentation.

****************
Adding a Feature
****************

The main features of CMinx are showcased in the ``docs/source/documenting``
folder. When a new feature is added to this folder along with an example. Code
for the examples should live in the ``tests/test_samples/`` directory in an
appropriately named file. You should also run CMinx on the sample file and put
the generated ``.rst`` file in ``tests/test_samples/corr_rst/``.

The contents of the cmake file are then included in the documentation ``.rst``
file like:

.. code::

   .. literalinclude:: ../../../tests/test_samples/your_example.cmake
      :language: cmake

and you can include the generated reST like:

.. code::

   .. literalinclude:: ../../../tests/test_samples/corr_rst/your_example.rst
      :language: rst

Following this process ensures that your example gets unit tested, and that the
documentation stays up to date.
