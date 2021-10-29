
####################
prefix.example.cmake
####################

.. module:: prefix.example.cmake


.. function:: say_hi_to(person me)
   
   This function has very basic documentation.
   
   This function's description stays close to idealized formatting and does not do
   anything fancy.
   
   :param person: The person this function says hi to
   :param me: What my name is
   :type person: string
   :type me: string
   


.. function:: macro_say_hi(person)

   .. warning:: This is a macro, and so does not introduce a new scope.

   
   This macro says hi.
   This documentation uses a differing format,
   but is still processed correctly.
   
   :param person: The person we want to greet.
   :type person: string 
   


.. data:: MyList
   
   This is an example of variable documentation.
   This variable is a list of string values.
   

   :Default value: ['"Value"', '"Value 2"']

   :type: VarType.List


.. data:: MyString
   
   This is another example of variable documentation.
   This variable is a string variable.
   

   :Default value: String

   :type: VarType.String

