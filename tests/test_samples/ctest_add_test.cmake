#[[[
# This is how to document a CTest test.
# Note that this is not a CMakeTest,
# but rather a vanilla CMake add_test() command.
#]]
add_test(
    NAME example_test
    COMMAND echo hello
    WORKING_DIRECTORY build/
)