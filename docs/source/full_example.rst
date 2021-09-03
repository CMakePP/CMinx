#######
Example
#######

Here we show an example CMake file, called :code:`example.cmake`, that contains
doccomments documenting functions, macros, and variables.
The file contents are shown below.

example.cmake:


.. include:: ../../examples/example.cmake
   :literal:



To generate the documentation, we enter our system shell (example assumes 
Bash-like shell on a Unix-like system).

Generating documentation in directory :code:`output`:

.. code:: console

      foo@bar:~$ cminx -o output/ example.cmake
      Writing RST files to /home/foo/output
      Writing for file /home/foo/example.cmake
      Writing RST file /home/foo/output/example.rst

The resultant file :code: `output/example.rst`:

.. include:: ../../examples/sphinx/source/example.rst
   :literal:

Place this file in a Sphinx source directory and add it to your :code: `toctree`
to render it.
