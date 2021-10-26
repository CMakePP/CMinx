**********************
Documenting a Variable
**********************

CMinx supports documenting variables. The process is identical to documenting a
function or macro, except that the documentation comment proceeds a ``set``
command. An example:

.. literalinclude:: ../../../tests/test_samples/variable.cmake
   :language: cmake

which generates:

.. literalinclude:: ../../../tests/test_samples/corr_rst/variable.rst
