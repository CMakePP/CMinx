include_guard()

set(CMAKEDOC_SRC "${CMAKE_CURRENT_SOURCE_DIR}" CACHE FILEPATH "Location of CMinx")


#[[[
# Generate documentation RST from source CMake files.
#
# :param dir: Directory to search for source files. Can also be a single file.
# :type dir: dir
# :param output: Directory to store output
# :type output: dir
#]]
function(cminx_gen_rst _cgd_dir _cgd_output)
        if(${ARGC} GREATER 2)
            execute_process(COMMAND "${VENV_PYTHON_EXECUTABLE}" "${CMAKEDOC_SRC}/main.py" ${_cgd_dir} "-o" "${_cgd_output}" "-p" "${ARGV2}" WORKING_DIRECTORY "${CMAKEDOC_SRC}" OUTPUT_VARIABLE process_output ERROR_VARIABLE process_err RESULT_VARIABLE process_result)
        else()
            execute_process(COMMAND "${VENV_PYTHON_EXECUTABLE}" "${CMAKEDOC_SRC}/main.py" ${_cgd_dir} "-o" "${_cgd_output}" WORKING_DIRECTORY "${CMAKEDOC_SRC}" OUTPUT_VARIABLE process_output ERROR_VARIABLE process_err RESULT_VARIABLE process_result)

        endif()
	message("${process_output}")
        if(NOT process_result EQUAL 0)
            message(FATAL_ERROR "Failed to generate RST. Result code was: ${process_result}. Error output was: ${process_err}")
        endif()

endfunction()

#[[[
# Add a custom target to the makefile called "docs" that calls Sphinx.
# Sphinx is automatically installed in the virtual environment and the target
# automatically uses that installed instance.
#
# :param _cad_doc_dir: Root directory of the sphinx docs where the makefile is located.
# :type _cad_doc_dir: dir
# :param _cad_output_dir: Directory where built docs will be placed
# :type _cad_output_dir: dir
# :param _cad_sphinx_target: Requested build target for Sphinx docs. Most common is "html".
# :type _cad_sphinx_target: desc
#]]
function(cminx_add_docs_target _cad_doc_dir _cad_output_dir _cad_sphinx_target)
	add_custom_target(docs COMMAND make "${_cad_sphinx_target}" "BUILDDIR=${_cad_output_dir}" "SPHINXBUILD=${VENV_PYTHON_EXECUTABLE} -m sphinx" WORKING_DIRECTORY "${_cad_doc_dir}")
endfunction()

