
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
   


.. function:: func_kwargs(**kwargs)

   This is a function with **kwargs.
   


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
   
   **Additional Constructors**

   .. py:method:: CTOR(a, b)

      This is a constructor
      

      :param a: 

      :type a: int

      :param b: 

      :type b: int

   **Methods**

   .. py:method:: a_method(param_1, param_2)

      This is a method
      

      :param param_1: 

      :type param_1: str

      :param param_2: 

      :type param_2: MyClass


   .. py:method:: a_method_no_args()

      This is a method without arguments
      

   **Attributes**

   .. py:attribute:: myattr
      :value: "a string"

      :type: str
      
      This is an attribute. Use the type option
      at the top of the doccomment and a blank line
      after to document the attribute type.
      



.. py:class:: MyClass2

   Bases: :class:`MyClass`
   
   This is another class with a superclass
   
   **Additional Constructors**

   .. py:method:: CTOR(a, b)

      This is a constructor
      

      :param a: 

      :type a: int

      :param b: 

      :type b: int

   **Methods**

   .. py:method:: a_method(param_1, param_2)

      This is a method
      

      :param param_1: 

      :type param_1: str

      :param param_2: 

      :type param_2: MyClass2

   **Attributes**

   .. py:attribute:: myattr
      :value: "a string"

      This is an attribute
      

   **Inner classes**

   * :class:`MyClass3`



.. py:class:: MyClass3

   This is a nested class
   
   **Additional Constructors**

   .. py:method:: CTOR(a, b)

      This is a constructor
      

      :param a: 

      :type a: int

      :param b: 

      :type b: int

   **Methods**

   .. py:method:: a_method(param_1, param_2)

      This is a method
      

      :param param_1: 

      :type param_1: str

      :param param_2: 

      :type param_2: MyClass3

   **Attributes**

   .. py:attribute:: myattr
      :value: "a string"

      This is an attribute
      



.. function:: undocumented_function()

   


.. function:: undocumented_macro()


   .. note:: This is a macro, and so does not introduce a new scope.

   


.. py:class:: MyClass

   
   **Additional Constructors**

   .. py:method:: CTOR()

      


   .. py:method:: CTOR2()


      .. note:: This member is a macro and so does not introduce a new scope

      

   **Methods**

   .. py:method:: undocced_function_member()

      


   .. py:method:: undocced_macro_member()


      .. note:: This member is a macro and so does not introduce a new scope

      

   **Attributes**

   .. py:attribute:: undocumented_attribute

      



.. function:: undocumented_test()


   .. warning:: This is a CMakeTest test definition, do not call this manually.

   


.. function:: undocumented_section()


   .. warning:: This is a CMakeTest section definition, do not call this manually.

   


.. function:: ctest_test(COMMAND bash -c echo test)


   .. warning:: This is a CTest test definition, do not call this manually. Use the "ctest" program to execute this test.

   This is a documented CTest test.
   Note that this is a vanilla CMake
   add_test() command, not a ct_add_test()
   command
   


.. function:: ctest_test_undocumented(COMMAND bash -c echo test)


   .. warning:: This is a CTest test definition, do not call this manually. Use the "ctest" program to execute this test.

   


.. data:: TEST_OPTION


   .. note:: 

      
                  This variable is a user-editable option,
                  meaning it appears within the cache and can be
                  edited on the command line by the :code:`-D` flag.
                  

   This is a documented option
   

   :Help text: "This is a test option"

   :Default value: OFF

   :type: bool

