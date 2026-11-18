.. Copyright 2024 CMakePP
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
**********************************
Excluding Code from Documentation
**********************************

A line starting with the :code:`@no-doc` directive in a doccomment excludes
the documented command from the generated documentation. When the command
starts a block, such as :code:`function()`, :code:`macro()` or
:code:`cpp_class()`, the whole block is excluded, including any documented
commands inside it. This also applies when undocumented commands are
included through the :code:`include_undocumented_*` settings.

.. literalinclude:: ../../../tests/test_samples/no_doc.cmake
   :language: cmake

For commands implemented by the :code:`function()` or :code:`macro()` that
follows them, such as :code:`ct_add_test()`, :code:`ct_add_section()`,
:code:`cpp_member()` and :code:`cpp_constructor()`, the following definition
is excluded as well.

To exclude a whole file, put :code:`@no-doc` in the first doccomment of the
file without attaching it to a command, or in the module doccomment. No page
is generated for the file, and it is left out of its directory's
:code:`index.rst`. A :code:`@no-doc` doccomment anywhere else that is not
attached to a command is an error.

.. note::

   Blank lines do not separate a doccomment from the command after it. If the
   first doccomment of the file is followed by a command, even after blank
   lines, :code:`@no-doc` excludes only that command rather than the file.
   To reliably exclude a whole file, put :code:`@no-doc` in a module
   doccomment at the top of the file:

   .. code-block:: cmake

      #[[[ @module
      # @no-doc
      #]]

      include_guard()
