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
####################
CMinx Repo Structure
####################

The purpose of this page is to briefly explain what the various directories and
files are for. We are primarily interested in infrastructure and not the actual
source code of CMinx. It is our hope that the contents of this page make it
easier for future developers to figure out where to put files and/or to figure
out what files may need to change for future updates.

.. note::

   If you are adding to this document please keep files and/or directories in
   the order they are likely to be displayed to the user. For the most part that
   is case-insensitive alphabetical order with directories listed before files.

*********
Top Level
*********

The top-level of the CMinx repo is the directory you get when you clone CMinx.
The top-level directory contains the following files:

- ``.gitignore`` Used by git to determine which files/folders should be version
  controlled
- ``CMakeLists.txt`` Entry point for building CMinx with CMake.
- ``codecov.yml`` Settings for `Codecov <https://about.codecov.io/>`__
- ``LICENSE`` Obligatory software license.
- ``main.py``
- ``README.md`` Text users are treated to when the visit the GitHub repo.
- ``requirements.txt`` Used by `pip` to install the correct dependencies.
- ``setup.py`` Entry point for
  `setuptools <https://setuptools.pypa.io/en/latest/>`, which is in turn used to
  build and install CMinx

and the following directories:

- ``.github`` Contains GitHub workflows, and settings, which constitute the CI
  testing of CMinx
- ``cmake`` assets needed to support the building CMinx with CMake
- ``cminx`` contains the source code for the CMinx executable
- ``docs`` contains the source code for CMinx's documentation
- ``tests`` contains source code for testing CMinx
