#[[[
# This macro says hi.
# This documentation uses a differing format,
# but is still processed correctly.
#
# :param person: The person we want to greet.
# :type person: string
#]]
macro(macro_say_hi person)
   message("Hi ${person}")
endmacro()
