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
#############################
Example CMinx/Sphinx Workflow
#############################

The purpose of this page is to show a start to finish example of how to use
CMinx and Sphinx to generate documentation. For the purposes of this tutorial
we assume:

- your project has a root directory ``example/``,
- ``example/docs/`` contains (or will contain) the source for the documentation,
- ``example/cmake/`` contains CMake modules, and
- ``example/cmake/example.cmake`` is the documented CMake source file

Summarily we assume a project structure:

.. code::

   └─ example/
      ├─ docs/
      └─ cmake/
         └─ example.cmake

For the purposes of this tutorial the contents of ``example.cmake`` is not too
important and we opt for a very basic CMake module:

.. include:: ../../tests/examples/basic_function.cmake
   :literal:

********************
Step 0: Dependencies
********************

This tutorial assumes you have already installed:

- Sphinx
  (`install <https://www.sphinx-doc.org/en/master/usage/installation.html>`__
  instructions)
- CMinx (:ref:`install <installing_cminx>` instructions)

and that they are in your path.

**************************************
Step 1: Initialize the docs/ Directory
**************************************

This step focuses on setting up the ``docs/`` directory for Sphinx-based
documentation. If your ``docs/`` directory is already setup feel free to skip
this step. In the ``docs/`` directory run:


.. code:: console

      foo@bar:example/docs$ sphinx-quickstart

and answer the questions according to your preferences (we highly recommend
separating the source and build directory). Afterwards you should have a
directory structure like (assuming you selected separate source and build
directories):

.. code::

   └─ example/
      ├─ docs/
      |  ├─ build/
      |  ├─ make.bat
      |  ├─ Makefile
      |  └─ source/
      |     ├─ conf.py
      |     ├─ index.rst
      |     ├─ _static/
      |     └─ _templates/
      └─ cmake/
         └─ example.cmake

************************
Step 2: Update index.rst
************************

When we run CMinx it will generate a directory filled with API documentation
for our CMake module. We need to decide where to put that directory. There are
many possibilities, but we recommend a directory in ``example/docs/source``
which is used to specifically house the API documentation
(*e.g.*, ``example/docs/source/cmake_api``).

Regardless of where you choose to put the generated files, the next step is to
modify ``example/docs/source/index.rst`` so that the documentation Sphinx generates
properly links to the API documentation. The default contents of ``index.rst``
will look something like:

.. code-block:: rst
   :linenos:

   .. example documentation master file, created by
      sphinx-quickstart on Thu Sep  1 13:11:45 2022.
      You can adapt this file completely to your liking, but it should at least
      contain the root `toctree` directive.

   Welcome to xxx's documentation!
   ===============================

   .. toctree::
      :maxdepth: 2
      :caption: Contents:



   Indices and tables
   ==================

   * :ref:`genindex`
   * :ref:`modindex`
   * :ref:`search`

Assuming you decide you too would like to put your API documentation in
``example/docs/source/cmake_api`` change line 13 to:

.. code-block:: rst

   cmake_api/example/index

(``example`` is the name of the CMake module without the ``.cmake`` extension).

.. note::

   As of this writing Sphinx does not allow you to reference out of a Sphinx
   project from inside a ``toctree`` directive (the root of a Sphinx project
   is defined by where the ``conf.py`` file lives). This means you can not
   put your generated API documentation in ``example/docs/build`` for example
   (at least without doing some dodgy stuff).

*****************
Step 3: Run CMinx
*****************

The next step is to run CMinx. There's a couple of ways to go about this so
choose the one that works best for your workflow.

Option 1: Manually run CMinx
============================

To generate the documentation, we enter our system shell (example assumes
Bash-like shell on a Unix-like system). Assuming CMinx is in our path we run
(in the root directory):

.. code:: console

      foo@bar:example$ cminx -o <output_dir> -r cmake

Where ``<output_dir>`` is the path to where you chose to put the API
documentation (``docs/source/cmake_api`` if you followed our suggestion
in step 2).


Option 2: Modify conf.py
========================

Another, arguably more convenient, option is to have Sphinx call CMinx as part
of building the documentation. To do this we modify the ``conf.py`` script
Sphinx generated. In particular we add:

.. code-block:: python

   import cminx
   cminx.main(['-o', '<output_dir>', '-r', '../../cmake])

to the ``conf.py`` file (where in ``conf.py`` is somewhat irrelevant, but its
usually added as some of the first lines of code). Note that the paths to
``cminx.main()`` are relative to the location of the ``conf.py`` file.

Option 3: Call CMinx from CMake
===============================

It is also possible to integrate CMinx into an existing build system. This is
most easily done via CMake's
`FetchContent <https://cmake.org/cmake/help/latest/module/FetchContent.html>`__
module.

.. code-block:: cmake

   include(FetchContent)
   FetchContent_Declare(
       cminx
       GIT_REPOSITORY https://github.com/cmakepp/cminx.git
   )
   FetchContent_MakeAvailable(cminx)
   cminx_gen_rst("${CMAKE_CURRENT_LIST_DIR}/cmake" "${output_dir}")

This assumes that the CMake script is located in the root directory of your
repository.

******************
Step 4: Run Sphinx
******************

Regardless of which option you chose in Step 3, your directory structure should
now look like (still assuming you have taken our recommendations along the
way):

.. code::

   └─ example/
      ├─ docs/
      |  ├─ build/
      |  ├─ make.bat
      |  ├─ Makefile
      |  └─ source/
      |     ├─ cmake_api/
      |     |  └─ example/
      |     |     ├─ example.rst
      |     |     └─ index.rst
      |     ├─ conf.py
      |     ├─ index.rst
      |     ├─ _static/
      |     └─ _templates/
      └─ cmake/
         └─ example.cmake

We are now finally read to generate the documentation. To do so, run
(in ``example/docs``):

.. code:: console

   foo@bar:example/docs$ make html

The index of the resulting website will live at
``example/docs/build/html/index.html``.
