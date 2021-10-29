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

When installing CMinx Pythonically, we strongly recommend you use a virtual 
environment. To obtain the CMinx source code and setup the virtual environment
run the following commands, one at a time, in a terminal:

.. code:: console

   foo@bar:~$ git clone https://github.com/CMakePP/CMinx.git
   foo@bar:~$ cd CMinx/
   foo@bar:~/CMinx$ python3 -m venv virt-env #Create our virtual environment
   foo@bar:~/CMinx$ source virt-env/bin/activate #Activate virtual environment

To finish off the installation using PIP run:

.. code:: console

   (virt-env) foo@bar:~/CMinx$ pip3 install wheel
   (virt-env) foo@bar:~/CMinx$ pip3 install .

or if you prefer to install without PIP run:

.. code:: console

   (virt-env) foo@bar:~/CMinx$ python3 setup.py install #If pip not installed

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