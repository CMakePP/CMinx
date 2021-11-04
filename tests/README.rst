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
###########
CMinx Tests
###########

The ``tests`` directory contains files related to testing CMinx and the code
snippets found in the documentation.

******************************
Building and Running the Tests
******************************

The unit tests are ready to run right out of the box. Simply run:

.. code::

   python3 test_all.py

******************
Directory Overview
******************

examples
========

This directory contains examples of how to write CMinx documentation, and  how
to use the Python classes which are part of CMinx. Compared to the content in
the ``test_samples`` directory, the contents of ``examples`` are meant to be
more tutorial like whereas the contents of ``test_samples`` are more
snippet-like.

test_samples
============

This directory contains the code snippets used throughout the documentation to
demonstrate CMinx features. Also included for each snippet is the reST which
results from running CMinx on the snippet.

unit_tests
==========

This directory contains unit tests for the Python classes and functions
comprising CMinx.
