find_package(CMinx
             ${PROJECT_VERSION}
             PATHS "${CMINX_STAGE_DIR}"
             NO_DEFAULT_PATH
             REQUIRED
             CONFIG
)

set(cwd "${CMAKE_CURRENT_LIST_DIR}")


################################################
# Defines needed macros for setup and teardown #
################################################

#[[[
# Sets needed variables for tests to function.
#]]
macro(do_setup)
  set(input_dir "${cwd}/../cmake_input")
  set(output_dir "${cwd}/output")
  set(input_file "${input_dir}/example.cmake")
  set(output_file "${output_dir}/example.rst")
endmacro()

#[[[
# Removes output directory after each test.
# Must be manually called, CMakeTest has no
# built-in teardown functiionality.
#]]
macro(do_teardown)
  file(REMOVE_RECURSE ${output_dir})
endmacro()


##########################
# Begin test definitions #
##########################


ct_add_test(NAME test_gen_rst)
function(${test_gen_rst})

  #TODO: This is a hack
  set(config_file "${cwd}/../../src/cminx/config_default.yaml")

  ct_add_section(NAME test_document)
  function(${test_document})
    do_setup()
    cminx_gen_rst("${input_file}" "${output_dir}" "-s" "${config_file}")

    ct_assert_file_exists("${output_file}")

    do_teardown()

  endfunction()

  ct_add_section(NAME test_document_prefix)
  function(${test_document_prefix})
    do_setup()
    cminx_gen_rst(
      "${input_file}" "${output_dir}" "-p" "input" "-s" "${config_file}"
    )

    ct_assert_file_exists("${output_file}")

    do_teardown()

  endfunction()

  ct_add_section(NAME test_document_recursive)
  function(${test_document_recursive})
    do_setup()
    cminx_gen_rst(
      "${input_dir}" "${output_dir}" "-s" "${config_file}"
    )

    ct_assert_file_exists("${output_file}")

    do_teardown()

  endfunction()


endfunction()
