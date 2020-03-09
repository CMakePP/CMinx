##########
Installing
##########


========
Manually
========

Run the following commands one at a time:

.. code:: console

   foo@bar:~$ git clone github.com/CMakePP/CMakeDoc.git
   foo@bar:~$ cd CMakeDoc/
   foo@bar:~/CMakeDoc$ python3 -m venv virt-env #Create our virtual environment
   foo@bar:~/CMakeDoc$ source virt-env/bin/activate #Activate virtual environment
   (virt-env) foo@bar:~/CMakeDoc$ pip3 install wheel #Necessary dependency to install manually with pip
   (virt-env) foo@bar:~/CMakeDoc$ pip3 install . #If pip installed
   (virt-env) foo@bar:~/CMakeDoc$ python3 setup.py install #If pip not installed

==========
With CMake
==========
Run:

.. code:: console

   foo@bar:~$ git clone github.com/CMakePP/CMakeDoc.git
   foo@bar:~$ cd CMakeDoc/
   foo@bar:~/CMakeDoc$ mkdir build && cd build
   foo@bar:~/CMakeDoc/build$ cmake ..
   foo@bar:~/CMakeDoc/build$ make install
