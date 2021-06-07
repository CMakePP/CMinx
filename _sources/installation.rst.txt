##########
Installing
##########


========
Manually
========

Run the following commands one at a time:

.. code:: console

   foo@bar:~$ git clone https://github.com/CMakePP/CMinx.git
   foo@bar:~$ cd CMinx/
   foo@bar:~/CMinx$ python3 -m venv virt-env #Create our virtual environment
   foo@bar:~/CMinx$ source virt-env/bin/activate #Activate virtual environment
   (virt-env) foo@bar:~/CMinx$ pip3 install wheel #Necessary dependency to install manually with pip
   (virt-env) foo@bar:~/CMinx$ pip3 install . #If pip installed
   (virt-env) foo@bar:~/CMinx$ python3 setup.py install #If pip not installed

==========
With CMake
==========
Run:

.. code:: console

   foo@bar:~$ git clone https://github.com/CMakePP/CMinx.git
   foo@bar:~$ cd CMinx/
   foo@bar:~/CMinx$ mkdir build && cd build
   foo@bar:~/CMinx/build$ cmake ..
   foo@bar:~/CMinx/build$ make install
