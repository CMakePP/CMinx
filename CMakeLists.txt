cmake_minimum_required(VERSION 3.12) #Python3 package locator only added in 3.12
set (CMAKE_MODULE_PATH "${CMAKE_MODULE_PATH};${CMAKE_CURRENT_SOURCE_DIR}/cmake")

file(STRINGS "${CMAKE_CURRENT_SOURCE_DIR}/version.txt" VERSION)

project(cmakedoc DESCRIPTION "CMake automatic documentation generator" LANGUAGES NONE VERSION ${VERSION}) #Not using any compiled languages so don't list, removes check for compilers

include(find_python_module)



find_package(Python3 COMPONENTS Interpreter REQUIRED)


#We have Python, now let's check to see if we have setuptools
find_python_module(setuptools REQUIRED)
find_python_module(venv REQUIRED)

set(SETUP_PY_IN "${CMAKE_CURRENT_SOURCE_DIR}/setup.py") #setup.py has logic to automatically switch between CMake variables and normal operation
set(SETUP_PY    "${CMAKE_CURRENT_BINARY_DIR}/setup.py")
set(DEPS        "${CMAKE_CURRENT_SOURCE_DIR}/cmakedoc/__init__.py")
set(OUTPUT      "${CMAKE_CURRENT_BINARY_DIR}/build/timestamp")


configure_file(${SETUP_PY_IN} ${SETUP_PY})

set(VENV "${CMAKE_CURRENT_BINARY_DIR}/virtual-env")

execute_process(COMMAND "${Python3_EXECUTABLE}" "-m" 
                        "venv" "${VENV}"
                        RESULT_VARIABLE _venv_status 
                        ERROR_QUIET OUTPUT_STRIP_TRAILING_WHITESPACE)

if (NOT _venv_status EQUAL "0")
	message(FATAL_ERROR "Virtual environment could not be created, venv returned ${_venv_status}")
endif()

set(VENV_PYTHON_EXECUTABLE "${VENV}/bin/python3")
set(VENV_PIP "${VENV}/bin/pip3")

execute_process(COMMAND "${VENV_PIP}" "install" "pyinstaller" "wheel") #Install our build tool to our build environment
execute_process(COMMAND "${VENV_PIP}" "install" "-e" "${CMAKE_CURRENT_BINARY_DIR}") #This "installs" the program in our build directory, in editable mode, meaning really only the dependencies are installed so that pyinstaller can find them




add_custom_command(OUTPUT ${OUTPUT}
                   COMMAND ${VENV_PYTHON_EXECUTABLE} "-m" "PyInstaller" "--onefile" "${CMAKE_CURRENT_SOURCE_DIR}/main.py" "--distpath=${CMAKE_CURRENT_BINARY_DIR}/dist" "--runtime-tmpdir=${CMAKE_INSTALL_PREFIX}/bin/.cmakedoc"
                   COMMAND "sh" "-c" "mkdir -p ${CMAKE_INSTALL_PREFIX}/bin/.cmakedoc" #Creates bin and .cmakedoc if needed
                   COMMAND "sh" "-c" "cp ${CMAKE_CURRENT_BINARY_DIR}/dist/main ${CMAKE_INSTALL_PREFIX}/bin/cmakedoc"
                   COMMAND ${CMAKE_COMMAND} -E touch ${OUTPUT}
                   DEPENDS ${DEPS})

add_custom_target(target ALL DEPENDS ${OUTPUT})

install(TARGETS RUNTIME)
