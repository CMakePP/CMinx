
################
examples.example
################

.. module:: examples.example


.. function:: say_hi_to(person me)

   This function has very basic documentation.
   
   This function's description stays close to idealized formatting and does not do
   anything fancy.
   
   :param person: The person this function says hi to
   :param me: What my name is
   :type person: string
   :type me: string
   


.. function:: macro_say_hi(person)


   .. note:: This is a macro, and so does not introduce a new scope.

   This macro says hi.
   This documentation uses a differing format,
   but is still processed correctly.
   
   :param person: The person we want to greet.
   :type person: string
   


.. function:: "${MyFunctionName}"()

   This is a documented function, but the name
   is dynamically assigned.
   


.. function:: "function_with_var_param_name"("${MyFunctionParamName}")

   This is a documented function, but the first parameter name
   is dynamically assigned.
   


.. function:: "${MyMacroName}"()


   .. note:: This is a macro, and so does not introduce a new scope.

   This is a documented macro, but the name
   is dynamically assigned.
   


.. function:: "macro_with_var_param_name"("${MyMacroParamName}")

   This is a documented macro, but the first parameter name
   is dynamically assigned.
   


.. data:: MyList

   This is an example of variable documentation.
   This variable is a list of string values.
   

   :Default value: "Value" "Value 2"

   :type: list


.. data:: MyString

   This is another example of variable documentation.
   This variable is a string variable.
   

   :Default value: String

   :type: str


.. function:: message("hello")


   .. warning:: This is a generic command invocation. It is not a function or macro definition.

   This is a generic command invocation.
   It will be documented as well, but with an admonition
   stating it is an invocation and not a definition.
   


.. py:class:: MyClass

   This is a class
   
   **Inner classes**

   * :class:`MyClass2`



.. py:class:: MyClass2

   Bases: :class:`MyClass`
   
   This is another class with a superclass
   


.. py:class:: MyClass3

   This is a nested class
   

