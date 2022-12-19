
##############################
test_samples.advanced_function
##############################

.. module:: test_samples.advanced_function


.. function:: advanced_say_hi_to(me **kwargs)

   Variation of say_hi_to, which takes lists of people and cats to say hi to.
   
   This function is basically the same as ``say_hi_to``, but accounts for the
   fact that you may want to say hi to multiple people and maybe even a cat or
   two.
   
   :param me: The name of the person saying hi.
   :type me: string
   
   **Keyword Arguments**
   
   :keyword PERSONS: The person or persons to say hi to.
   :type PERSONS: list of strings
   :keyword CATS: The cat or cats to say hi to.
   :type CATS: list of strings
   

