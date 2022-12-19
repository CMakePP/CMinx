
###########################
test_samples.advanced_macro
###########################

.. module:: test_samples.advanced_macro


.. function:: advanced_macro_say_hi(me **kwargs)


   .. note:: This is a macro, and so does not introduce a new scope.

   Variation of macro_say_hi, which takes lists of people and cats to say hi to.
   
   This macro is basically the same as ``macro_say_hi``, but accounts for the
   fact that you may want to say hi to multiple people and maybe even a cat or
   two.
   
   :param me: The name of the person saying hi.
   :type me: string
   
   **Keyword Arguments**
   
   :keyword PERSONS: The person or persons to say hi to.
   :type PERSONS: list of strings
   :keyword CATS: The cat or cats to say hi to.
   :type CATS: list of strings
   

