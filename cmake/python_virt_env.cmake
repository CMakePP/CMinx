include_guard()

#[[[
# Wraps the process of creating a virtual Python environment.
#
# :param mpv_exe: The Python interpreter to use to make the virtual environment
# :param mpv_venv: The full path to the virtual environment
#]]
function(make_python_venv mpv_exe mpv_venv)
    message(STATUS "Creating Python virtual environment: ${mpv_venv}")
    execute_process(
        COMMAND "${mpv_exe}" "-m" "venv" "${mpv_venv}"
        RESULT_VARIABLE _venv_status
        ERROR_QUIET OUTPUT_STRIP_TRAILING_WHITESPACE
    )

    if (NOT _venv_status EQUAL "0")
	    message(
            FATAL_ERROR
            "Virtual environment could not be created, venv "
            "returned ${_venv_status}"
        )
    endif()
endfunction()

#[[[
# Wraps the process of installing a Python module into a virtual Python
# environment, via pip.
#
# :param pvpi_venv: The full path to the Python virtual environment into which
#                   we are installing the Python module.
# :param pvpi_module: The name of the pip package we are installing.
#
#]]
function(python_venv_pip_install pvpi_venv pvpi_module)
    message(STATUS "Installing ${pvpi_module} in ${pvpi_venv}")
    set(_pvpi_pip ${pvpi_venv}/bin/pip3)
    execute_process(
        COMMAND "${_pvpi_pip}" "install" "${pvpi_module}"
    )
endfunction()
