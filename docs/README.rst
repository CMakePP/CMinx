##############################
Documentation Source for CMinx
##############################

This directory contains the source for CMinx's documentation. CMinx's
documentation depends on:

- Python3
- Sphinx
- Sphinx Read-the-Docs Theme

with the exception of Python itself, all other dependencies are available from
PIP (Python is likely available from your operating system's package manager).

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
