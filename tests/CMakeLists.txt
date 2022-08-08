
################################################################################
# Test CMinx's CMake Infrastructure
################################################################################

#Sets print length to cached variable. This value is propagated
#to all tests but can be overriden with subsequent calls or
#via PRINT_LENGTH option to ct_add_test() and ct_add_section()
#Added for user convenience.
set(
    CT_DEFAULT_PRINT_LENGTH 80
    CACHE
    STRING
    "The default print length for pass/fail lines. Can be overriden by
      individual tests."
)
ct_set_print_length("${CT_DEFAULT_PRINT_LENGTH}")

ct_add_dir(
    "cmake"
    CMAKE_OPTIONS "-DCMINX_STAGE_DIR=${CMINX_STAGE_DIR}"
                  "-DPROJECT_VERSION=${PROJECT_VERSION}"
)

################################################################################
# Test CMinx Itself
################################################################################

add_test(
    NAME "CMinx_Unit_Tests"
    COMMAND "${CMINX_VENV}/bin/python3" "-B" "test_all.py"
    WORKING_DIRECTORY "${CMAKE_CURRENT_LIST_DIR}"
)
