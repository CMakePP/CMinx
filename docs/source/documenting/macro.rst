###################
Documenting a Macro
###################

From the perspective of a CMinx user, one documents a macro in the same manner
as a function. For example:

.. literalinclude:: ../../../tests/test_samples/basic_macro.cmake
   :language: cmake

Since macros and functions behave differently in CMake (the biggest difference
being that functions introduce a new scope, whereas macros do not). CMinx will
automatically note in the generated documentation whether the command being
documented is a function or a macro.

.. literalinclude:: ../../../tests/test_samples/corr_rst/basic_macro.rst
   :language: rst
