#################
Documenting CMinx
#################

This page contains notes for developers on how to update the CMinx
documentation.

****************
Adding a Feature
****************

The main features of CMinx are showcased in the ``docs/source/documenting``
folder. When a new feature is added to this folder along with an example. Code
for the examples should live in the ``tests/test_samples/`` directory in an
appropriately named file. You should also run CMinx on the sample file and put
the generated ``.rst`` file in ``tests/test_samples/corr_rst/``.

The contents of the cmake file are then included in the documentation ``.rst``
file like:

.. code::

   .. literalinclude:: ../../../tests/test_samples/your_example.cmake
      :language: cmake

and you can include the generated reST like:

.. code::

   .. literalinclude:: ../../../tests/test_samples/corr_rst/your_example.rst
      :language: rst

Following this process ensures that your example gets unit tested, and that the
documentation stays up to date.
