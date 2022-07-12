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
##########
CMinx's CI
##########

This page is meant to be a place for developer's to put notes etc. pertaining to
maintaining CMinx's CI.

*******
Linting
*******

The workflow ``.github/workflows/format_python.yaml`` manages the linting of
Python source code. It covers linting CMinx proper as well as linting the test
suite. By design the workflow runs on each PR, and pushes the changes back to
the PR. This ensures that the master branch is always properly formatted.
