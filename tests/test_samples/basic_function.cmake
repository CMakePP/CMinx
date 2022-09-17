include_guard()

#[[[
# This function has very basic documentation.
#
# This function's description stays close to idealized formatting and does not
# do anything fancy.
#
# :param person: The person this function says hi to
# :type person: string
#]]
function(say_hi_to person)
    message("Hi ${person}")
endfunction()
