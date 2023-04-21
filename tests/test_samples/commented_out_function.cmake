#[[[ @module
# This is a module containing a commented-out function
#]]
# This is a line comment

#[[[
# Properly documented command
#]]
function(test1)
endfunction()
#[[[
# Documenting a commented-out function should not blow up
#]]
#function(test)
#
#endfunction()