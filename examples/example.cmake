#[[
# THIS SHOULD BE SKIPPED
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
# This macro says hi
#]]
macro(macro_say_hi person)
   message("Hi ${person}")
endmacro()


#[[[
# list
#]]
set(MyList "Value" "Value 2")


#[[[
# string
#]]
set(MyString "String")
