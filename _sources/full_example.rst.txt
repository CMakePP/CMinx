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
################
Example Workflow
################

Here we show a start to finish example of using CMinx. We assume you have a
CMake file, called :code:`example.cmake`, in your current directory. The
contents of :code:`example.cmake` are:

.. include:: ../../tests/examples/example.cmake
   :literal:

To generate the documentation, we enter our system shell (example assumes
Bash-like shell on a Unix-like system). Assuming CMinx is in our path and we
want to generate the documentation in the directory :code:`output`, we run:

.. code:: console

      foo@bar:~$ cminx -o output/ example.cmake
      Writing RST files to /home/foo/output
      Writing for file /home/foo/example.cmake
      Writing RST file /home/foo/output/example.rst

The resultant file :code:`output/example.rst`:

.. include:: ../../tests/examples/sphinx/source/example.rst
   :literal:

Place this file in a Sphinx source directory and add it to your :code:`toctree`
to render it.
