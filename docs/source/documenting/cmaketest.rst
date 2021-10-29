############################
Documenting a CMakeTest Test
############################

CMinx can be used to document
`CMakeTest <https://github.com/CMakePP/CMakeTest>`_ tests and test sections.
Again, this is done analogous to other documentation use cases, *i.e.*, by
proceeding the ``ct_add_test`` or ``ct_add_section`` command with a
documentation comment. For example,

.. literalinclude:: ../../../tests/test_samples/ct_test.cmake
   :language: cmake

which generates:

.. literalinclude:: ../../../tests/test_samples/corr_rst/ct_test.rst
   :language: rst
