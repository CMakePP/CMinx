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

.. _installing_cminx:

##########
Installing
##########

CMinx is ultimately a Python package designed to be used as part of a C/C++
workflow. For this reason we provide two ways of installing CMinx: using normal
Python channels and via normal CMake channels. Functionally the two install
methods should produce equivalent results and the choice of which to use is
purely personal preference.

************
Pythonically
************

Unless you are developing CMinx we recommend you install CMinx from PyPI.
From a terminal this is simply:

.. code:: console

   foo@bar:~$ pip install CMinx

If you are developing CMinx then we recommend doing an editable install of
CMinx in a virtual environment:

.. code:: console

   foo@bar:~$ git clone https://github.com/CMakePP/CMinx.git
   foo@bar:~$ cd CMinx/
   foo@bar:~/CMinx$ python3 -m venv virt-env #Create our virtual environment
   foo@bar:~/CMinx$ source virt-env/bin/activate #Activate virtual environment
   (virt-env) foo@bar:~/CMinx$ pip3 install -e .

**********
With CMake
**********

Installing CMinx with CMake follows the usual CMake workflow, namely, run the
following commands, one at a time, in a terminal:

.. code:: console

   foo@bar:~$ git clone https://github.com/CMakePP/CMinx.git
   foo@bar:~$ cd CMinx/
   foo@bar:~/CMinx$ cmake -S . -B <build_dir>
   foo@bar:~/CMinx$ cmake --build <build_dir>
   foo@bar:~/CMinx$ cmake --install <build_dir>

where ``<build_dir>`` should be substituted for the name of the directory you
want CMake to use for building.

The CMake build of CMinx honors relevant CMake variables. In particular:

CMAKE_INSTALL_PREFIX
   Can be used to control where CMinx is installed. It is recommended that users
   use full paths. Given the path `/where/cminx/should/go` the actual CMinx
   executable will live at `/where/cminx/should/go/bin/cminx`
