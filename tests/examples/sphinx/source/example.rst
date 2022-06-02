
#######
example
#######

.. module:: example


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


.. function:: message("hello")


   .. warning:: This is a generic command invocation. It is not a function or macro definition.

   This is a generic command invocation.
   It will be documented as well, but with an admonition
   stating it is an invocation and not a definition.
   


.. py:class:: MyClass

   This is a class
   

   .. py:attribute:: myattr
      :value: "a string"

      :type: str
      
      This is an attribute. Use the type option
      at the top of the doccomment and a blank line
      after to document the attribute type.
      


   .. py:method:: a_method(param_1, param_2)

      This is a method
      

      :param param_1: 

      :type param_1: str

      :param param_2: 

      :type param_2: MyClass


   .. py:method:: a_method_no_args()

      This is a method without arguments
      


   .. py:method:: CTOR(a, b)


      .. admonition:: info

         This member is a constructor.

      This is a constructor
      

      :param a: 

      :type a: int

      :param b: 

      :type b: int



.. py:class:: MyClass2

   This is another class
   

   .. py:attribute:: myattr
      :value: "a string"

      This is an attribute
      


   .. py:method:: a_method(param_1, param_2)

      This is a method
      

      :param param_1: 

      :type param_1: str

      :param param_2: 

      :type param_2: MyClass2


   .. py:method:: CTOR(a, b)


      .. admonition:: info

         This member is a constructor.

      This is a constructor
      

      :param a: 

      :type a: int

      :param b: 

      :type b: int



.. py:class:: MyClass3

   This is a nested class
   

   .. py:attribute:: myattr
      :value: "a string"

      This is an attribute
      


   .. py:method:: a_method(param_1, param_2)

      This is a method
      

      :param param_1: 

      :type param_1: str

      :param param_2: 

      :type param_2: MyClass3


   .. py:method:: CTOR(a, b)


      .. admonition:: info

         This member is a constructor.

      This is a constructor
      

      :param a: 

      :type a: int

      :param b: 

      :type b: int


