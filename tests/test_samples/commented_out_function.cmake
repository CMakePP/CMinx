#[[[ @module
# This is a module containing a commented-out function
#]]
# This is a line comment

#[[[
# Properly documented command
#
# :param param1: This is a parameter
# :type param1: str
# :param param2: This is another parameter
# :type param2: desc
#]]
function(test1 param1 param2)
endfunction()
#[[[
# Documenting a commented-out function should not blow up
#
# :param param3: This is a parameter
# :type param3: str
# :param param4: This is another parameter
# :type param4: desc
#]]
#function(test param3 param4)
#
#endfunction()