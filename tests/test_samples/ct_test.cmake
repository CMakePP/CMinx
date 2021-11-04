#[[[
# This is how you document a CMakeTest test.
#]]
ct_add_test(NAME test1 EXPECTFAIL)
function(${test1})

    #[[[
    # And this is how you document a CMakeTest section.
    #]]
    ct_add_section(NAME section1 EXPECTFAIL)
    function(${section1})
    endfunction()

endfunction()
