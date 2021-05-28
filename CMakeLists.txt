cmake_minimum_required(VERSION 3.12) #Python3 package locator only added in 3.12
set (CMAKE_MODULE_PATH "${CMAKE_MODULE_PATH};${CMAKE_CURRENT_SOURCE_DIR}/cmake")

file(STRINGS "${CMAKE_CURRENT_SOURCE_DIR}/version.txt" VERSION)

project(cminx DESCRIPTION "CMake automatic documentation generator" LANGUAGES NONE VERSION ${VERSION}) #Not using any compiled languages so don't list, removes check for compilers


#Allows us to locate any arbitrary Python3 module.
include(find_python_module)



find_package(Python3 COMPONENTS Interpreter REQUIRED)


#We have Python, now let's check to see if we have setuptools and venv
find_python_module(setuptools REQUIRED)
find_python_module(venv REQUIRED)

set(DEPS        "${CMAKE_CURRENT_SOURCE_DIR}/cminx/__init__.py")
set(OUTPUT      "${CMAKE_CURRENT_BINARY_DIR}/build/timestamp")


#[[[
# Points to the location of the build virtual environment.
#]]
set(VENV "${CMAKE_CURRENT_BINARY_DIR}/virtual-env")

#Create virtual environment in the build directory
message(STATUS "Creating virtual environment for build directory...")

execute_process(COMMAND "${Python3_EXECUTABLE}" "-m" 
                        "venv" "${VENV}"
                        RESULT_VARIABLE _venv_status 
                        ERROR_QUIET OUTPUT_STRIP_TRAILING_WHITESPACE)

if (NOT _venv_status EQUAL "0")
	message(FATAL_ERROR "Virtual environment could not be created, venv returned ${_venv_status}")
endif()

#[[[
# Location of the virtual environment python 3 executable.
#]]
set(VENV_PYTHON_EXECUTABLE "${VENV}/bin/python3")

#[[[
# Location of the virtual environment pip.
#]]
set(VENV_PIP "${VENV}/bin/pip3")

#Install needed dependencies
message(STATUS "Installing build dependencies in virtual environment...")

execute_process(COMMAND "${VENV_PIP}" "install" "pyinstaller") #Install our build tool to our build environment


#Install program specific dependencies so that pyinstaller can find them.
execute_process(COMMAND "${VENV_PIP}" "install" "-r" "${CMAKE_CURRENT_SOURCE_DIR}/requirements.txt")



#[[
# Installation command.
# First line calls PyInstaller to build the single file executable.
# Second line creates the necessary install directories.
# Third line copies the resultant executable to the installation path.
#]]
add_custom_command(OUTPUT ${OUTPUT}
                   COMMAND ${VENV_PYTHON_EXECUTABLE} "-m" "PyInstaller" "--onefile" "${CMAKE_CURRENT_SOURCE_DIR}/main.py" "--distpath=${CMAKE_CURRENT_BINARY_DIR}/dist" "--runtime-tmpdir=${CMAKE_INSTALL_PREFIX}/bin/.cminx"
                   COMMAND "sh" "-c" "mkdir -p ${CMAKE_INSTALL_PREFIX}/bin/.cminx" #Creates bin and .cminx if needed
                   COMMAND "sh" "-c" "cp ${CMAKE_CURRENT_BINARY_DIR}/dist/main ${CMAKE_INSTALL_PREFIX}/bin/cminx"
                   COMMAND ${CMAKE_COMMAND} -E touch ${OUTPUT}
                   DEPENDS ${DEPS})

add_custom_target(target ALL DEPENDS ${OUTPUT})

install(TARGETS RUNTIME)


include("cminx")
cminx_gen_rst("${CMAKE_CURRENT_SOURCE_DIR}/cmake/cminx.cmake" "${CMAKE_CURRENT_SOURCE_DIR}/docs/source/developer/cmake")

cminx_add_docs_target("${CMAKE_CURRENT_SOURCE_DIR}/docs" "${CMAKE_CURRENT_BINARY_DIR}/docs" html)
