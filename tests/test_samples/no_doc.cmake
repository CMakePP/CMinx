#[[[
# This function is documented.
#]]
function(documented_function)
endfunction()

#[[[
# @no-doc
#
# This function is an implementation detail, so it is not documented,
# along with any documented commands inside it.
#]]
function(_internal_function)
    #[[[
    # Not documented either.
    #]]
    set(internal_variable "")
endfunction()

#[[[
# @no-doc
#]]
option(INTERNAL_OPTION "Not documented" OFF)

#[[[
# Documentation resumes after the command or block.
#]]
set(documented_variable "")
