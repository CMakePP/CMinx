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