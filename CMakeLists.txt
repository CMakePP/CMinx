cmake_minimum_required(VERSION 3.12) #Python3 package locator only added in 3.12

project(cmakedoc DESCRIPTION "CMake automatic documentation generator" LANGUAGES NONE VERSION 1.0.0) #Not using any compiled languages so don't list, removes check for compilers

find_package(Python3 COMPONENTS Interpreter REQUIRED)

#[[[
# Custom function to locate a Python module. Requires the Python interpreter to be located first.
#
# Sets PY_${module_upper} to the module file's location if found.
#
# :param module: Python module name to locate
# :param REQUIRED: Optional paramater, specifies that this module is required for continued execution.
# Sets ${module}_FIND_REQUIRED to true.
#
#]]
function(find_python_module module)
        set(options REQUIRED)
        set(single_vals "")
        set(multi_vals "")
        cmake_parse_arguments(PYMODULE "${options}" "${single_vals}" "${multi_vals}" ${ARGN})

	string(TOUPPER ${module} module_upper)
	if(NOT PY_${module_upper})
		if(${PYMODULE_REQUIRED})
			set(${module}_FIND_REQUIRED TRUE)
		endif()
		# A module's location is usually a directory, but for binary modules
		# it's a .so file.
		execute_process(COMMAND "${Python3_EXECUTABLE}" "-c" 
			"import re, ${module}; print(re.compile('/__init__.py.*').sub('',${module}.__file__))"
			RESULT_VARIABLE _${module}_status 
			OUTPUT_VARIABLE _${module}_location
		        ERROR_QUIET OUTPUT_STRIP_TRAILING_WHITESPACE)
		if(NOT _${module}_status)
			set(PY_${module_upper} ${_${module}_location} CACHE STRING 
				"Location of Python module ${module}")
		endif(NOT _${module}_status)
	endif(NOT PY_${module_upper})
	find_package_handle_standard_args(PY_${module} DEFAULT_MSG PY_${module_upper})
endfunction(find_python_module)


#We have Python, now let's check to see if we have setuptools
find_python_module(setuptools REQUIRED)

if (PY_SETUPTOOLS)

    set(SETUP_PY_IN "${CMAKE_CURRENT_SOURCE_DIR}/setup.py") #setup.py has logic to automatically switch between CMake variables and normal operation
    set(SETUP_PY    "${CMAKE_CURRENT_BINARY_DIR}/setup.py")
    set(DEPS        "${CMAKE_CURRENT_SOURCE_DIR}/cmakedoc/__init__.py")
    set(OUTPUT      "${CMAKE_CURRENT_BINARY_DIR}/build/timestamp")

    configure_file(${SETUP_PY_IN} ${SETUP_PY})

    add_custom_command(OUTPUT ${OUTPUT}
                       COMMAND ${Python3_EXECUTABLE} ${SETUP_PY} build
                       COMMAND ${CMAKE_COMMAND} -E touch ${OUTPUT}
                       DEPENDS ${DEPS})

    add_custom_target(target ALL DEPENDS ${OUTPUT})

    install(CODE "execute_process(COMMAND ${PYTHON} ${SETUP_PY} install)")
else()
    message(FATAL_ERROR "setuptools Python3 package not installed")
endif()
