################
Example Workflow
################

Here we show a start to finish example of using CMinx. We assume you have a
CMake file, called :code:`example.cmake`, in your current directory. The
contents of :code:`example.cmake` are:

.. include:: ../../tests/test_samples/example.cmake
   :literal:

To generate the documentation, we enter our system shell (example assumes
Bash-like shell on a Unix-like system). Assuming CMinx is in our path and we
want to generate the documentation in the directory :code:`output`, we run:

.. code:: console

      foo@bar:~$ cminx -o output/ example.cmake
      Writing RST files to /home/foo/output
      Writing for file /home/foo/example.cmake
      Writing RST file /home/foo/output/example.rst

The resultant file :code:`output/example.rst`:

.. include:: ../../examples/sphinx/source/example.rst
   :literal:

Place this file in a Sphinx source directory and add it to your :code:`toctree`
to render it.
