#[[
# This is a normal block comment and will not
# be treated as a doccomment.
#]]
include_guard()

#[[[
# This function has very basic documentation.
#
# This function's description stays close to idealized formatting and does not do
# anything fancy.
#
# :param person: The person this function says hi to
# :param me: What my name is
# :type person: string
# :type me: string
#]]
function(say_hi_to person me)
    message("Hi ${person}, I am ${me}")
endfunction()

#[[[
This macro says hi.
This documentation uses a differing format,
but is still processed correctly.

:param person: The person we want to greet.
:type person: string
#]]
macro(macro_say_hi person)
   message("Hi ${person}")
endmacro()


#[[[
# This is an example of variable documentation.
# This variable is a list of string values.
#]]
set(MyList "Value" "Value 2")


#[[[
# This is another example of variable documentation.
# This variable is a string variable.
#]]
set(MyString "String")

#[[[
# This is a generic command invocation.
# It will be documented as well, but with an admonition
# stating it is an invocation and not a definition.
#]]
message("hello")

#[[[
# This is a class
#]]
cpp_class(MyClass)

    #[[[
    # :type: str
    #
    # This is an attribute. Use the type option
    # at the top of the doccomment and a blank line
    # after to document the attribute type.
    #]]
    cpp_attr(MyClass myattr "a string")

    #[[[
    # This is a method
    #]]
    cpp_member(a_method MyClass str MyClass)
    function(${a_method} self param_1 param_2)
        
    endfunction()

    #[[[
    # This is a constructor
    #]]
    cpp_constructor(CTOR MyClass int int)
    function("${CTOR}" self a b)
       # Do set up using arguments passed to constructors
    endfunction()


cpp_end_class()

#[[[
# This is another class
#]]
cpp_class(MyClass2)

    #[[[
    # This is an attribute
    #]]
    cpp_attr(MyClass2 myattr "a string")

    #[[[
    # This is a method
    #]]
    cpp_member(a_method MyClass2 str MyClass2)
    function(${a_method} self param_1 param_2)
        
    endfunction()

    #[[[
    # This is a constructor
    #]]
    cpp_constructor(CTOR MyClass2 int int)
    function("${CTOR}" self a b)
       # Do set up using arguments passed to constructors
    endfunction()

    #[[[
    # This is a nested class
    #]]
    cpp_class(MyClass3)

        #[[[
        # This is an attribute
        #]]
        cpp_attr(MyClass3 myattr "a string")

        #[[[
        # This is a method
        #]]
        cpp_member(a_method MyClass3 str MyClass3)
        function(${a_method} self param_1 param_2)
    
        endfunction()

        #[[[
        # This is a constructor
        #]]
        cpp_constructor(CTOR MyClass3 int int)
        function("${CTOR}" self a b)
            # Do set up using arguments passed to constructors
        endfunction()


    cpp_end_class()


cpp_end_class()
