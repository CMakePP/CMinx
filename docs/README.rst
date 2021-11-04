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
##############################
Documentation Source for CMinx
##############################

This directory contains the source for CMinx's documentation. CMinx's
documentation depends on:

- Python3
- Sphinx
- Sphinx Read-the-Docs Theme
- CMinx

with the exception of Python itself, and CMinx, all other dependencies are
available from PIP (Python is likely available from your operating system's
package manager; CMinx is the current repo).

**************************
Building the Documentation
**************************

Assuming you have Python3, the recommended workflow for building the
documentation is to run the following commands in a console:

.. code:: console

   foo@bar:~/CMinx/docs$ python3 -m venv virt_env
   foo@bar:~/CMinx/docs$ source virt_env/bin/activate
   (virt_env) foo@bar:~/CMinx/docs$ pip3 install -r requirements.txt
   (virt_env) foo@bar:~/CMinx/docs$ make html

The first two commands create and activate a Python virtual environment. The
third command installs the Python packages that the documentation depends on,
and the last command actually builds the documentation. The resulting
documentation will live in a directory called ``build``. If you would like the
documentation to be built somewhere else, instead of the last command run:

.. code:: console

   (virt_env) foo@bar:~/CMinx/docs$ make html BUILDDIR=/where/to/put/docs

*************************
Viewing the Documentation
*************************

Assuming the documentation lives in ``BUILDDIR``, the index page for the
documentation will be located at ``BUILDDIR/html/index.html``. You can view the
documentation by directing your internet browser to
``file://full/path/to/BUILDDIR/html/index.html``. The most up to date version of
the documentation is also hosted at `https://cmakepp.github.io/CMinx/`.
