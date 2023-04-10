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
# This is a function with **kwargs.
#]]
function(func_kwargs)
	cmake_parse_arguments(
		"func_kwargs"
		"OPTIONAL"
		${ARGN}
	)

endfunction()

set(MyFunctionName "Name_Of_A_Function")

#[[[
# This is a documented function, but the name
# is dynamically assigned.
#]]
function("${MyFunctionName}")
endfunction()

set(MyFunctionParamName "Name_Of_A_Param")

#[[[
# This is a documented function, but the first parameter name
# is dynamically assigned.
#]]
function("function_with_var_param_name" "${MyFunctionParamName}")
endfunction()



set(MyMacroName "Name_Of_A_Macro")

#[[[
# This is a documented macro, but the name
# is dynamically assigned.
#]]
macro("${MyMacroName}")
endmacro()

set(MyMacroParamName "Name_Of_A_Param")

#[[[
# This is a documented macro, but the first parameter name
# is dynamically assigned.
#]]
function("macro_with_var_param_name" "${MyMacroParamName}") 
endfunction()


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

#[[
# This is an undocumented variable.
# Unlike most other elements, it will
# not be automatically added to the documentation
# since there is no way to tell a local variable apart
# from a global property
#]]
set(MyUndocumentedVariable "Value")

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
    # This is a method without arguments
    #]]
    cpp_member(a_method_no_args MyClass)
    function(${a_method} self)
        
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
# This is another class with a superclass
#]]
cpp_class(MyClass2 MyClass)

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

#[[
# This is an undocumented function
#]]
function(undocumented_function)
endfunction()

#[[
# This is an undocumented macro
#]]
macro(undocumented_macro)
endmacro()

#[[
# This is an undocumented class
#]]
cpp_class(MyClass)

    # This is an undocumented function constructor
    cpp_constructor(CTOR MyClass)
    function("${CTOR}" self)
    endfunction()

    # This is an undocumented macro constructor
    cpp_constructor(CTOR2 MyClass)
    macro("${CTOR2}" self)
    endmacro()

    # This is an undocumented attribute
    cpp_attr(MyClass undocumented_attribute)

    # This is an undocumented function member
    cpp_member(undocced_function_member MyClass)
    function("${undocced_function_member}" self)
    endfunction()

    # This is an undocumented macro member
    cpp_member(undocced_macro_member MyClass)
    macro("${undocced_macro_member}" self)
    endmacro()

cpp_end_class()

# This is an undocumented test
ct_add_test(NAME undocumented_test)
function("${undocumented_test}")

    # This is an undocumented section
    ct_add_section(NAME undocumented_section)
    function("${undocumented_section}")
    endfunction()

endfunction()

#[[[
# This is a documented CTest test.
# Note that this is a vanilla CMake
# add_test() command, not a ct_add_test()
# command
#]]
add_test(
    NAME ctest_test
    COMMAND bash -c echo test
)

#[[
# This is an udocumented CTest test.
# Note that this is a vanilla CMake
# add_test() command, not a ct_add_test()
# command
#]]
add_test(
    NAME ctest_test_undocumented
    COMMAND bash -c echo test
)

#[[[
# This is a documented option
#]]
option(TEST_OPTION "This is a test option" OFF)

