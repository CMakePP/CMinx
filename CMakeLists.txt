cmake_minimum_required(VERSION 3.12) #Python3 package locator only added in 3.12
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")

file(STRINGS "${CMAKE_CURRENT_SOURCE_DIR}/version.txt" CMINX_VERSION)

#N.B. Not using a compiled language, by not setting we remove compiler checks
project(cminx
        DESCRIPTION "CMake automatic documentation generator"
        LANGUAGES NONE
        VERSION ${CMINX_VERSION}
)

option(BUILD_DOCS "Whether documentation targets should be added" OFF)
option(BUILD_TESTING "Whether tests should be built ad ctest configured" OFF)


#Allows us to locate any arbitrary Python3 module.
include(find_python_module)



find_package(Python3 COMPONENTS Interpreter REQUIRED)


#We have Python, now let's check to see if we have setuptools and venv
find_python_module(setuptools REQUIRED)
find_python_module(venv REQUIRED)

set(DEPS        "${CMAKE_CURRENT_SOURCE_DIR}/cminx/__init__.py")
set(OUTPUT      "${CMAKE_CURRENT_BINARY_DIR}/cminx")


#[[[
# Points to the location of the build virtual environment.
#]]
set(CMINX_VENV "${CMAKE_CURRENT_BINARY_DIR}/virtual-env" CACHE FILEPATH "Directory of the virtual environment")

#Create virtual environment in the build directory
message(STATUS "Creating virtual environment for build directory...")

execute_process(COMMAND "${Python3_EXECUTABLE}" "-m"
                        "venv" "${CMINX_VENV}"
                        RESULT_VARIABLE _venv_status
                        ERROR_QUIET OUTPUT_STRIP_TRAILING_WHITESPACE)

if (NOT _venv_status EQUAL "0")
	message(FATAL_ERROR "Virtual environment could not be created, venv returned ${_venv_status}")
endif()

#[[[
# Location of the virtual environment python 3 executable.
#]]
set(CMINX_VENV_PYTHON_EXECUTABLE "${CMINX_VENV}/bin/python3" CACHE FILEPATH "The location of the virtual environment Python3 executable.")

#[[[
# Location of the virtual environment pip.
#]]
set(CMINX_VENV_PIP "${CMINX_VENV}/bin/pip3" CACHE FILEPATH "The location of the Pip3 to be used for the virtual environment")

#Install needed dependencies
message(STATUS "Installing build dependencies in virtual environment...")

execute_process(COMMAND "${CMINX_VENV_PIP}" "install" "pyinstaller") #Install our build tool to our build environment


#Install program specific dependencies so that pyinstaller can find them.
execute_process(COMMAND "${CMINX_VENV_PIP}" "install" "-e" "${CMAKE_CURRENT_SOURCE_DIR}")

#Write package config files
configure_file("${CMAKE_CURRENT_LIST_DIR}/templates/CMinxConfig.cmake" "${CMAKE_CURRENT_BINARY_DIR}" @ONLY)
configure_file("${CMAKE_CURRENT_LIST_DIR}/templates/CMinxConfigVersion.cmake" "${CMAKE_CURRENT_BINARY_DIR}" @ONLY)
set(CMINX_PACKAGE_SEARCH_PATH "${CMAKE_CURRENT_BINARY_DIR}")

#[[
# Build command.
# First line calls PyInstaller to build the single file executable.
# Second line copies the resultant executable to the binary directory.
#]]
add_custom_target(cminx ALL
                   ${CMINX_VENV_PYTHON_EXECUTABLE} "-m" "PyInstaller" "--onefile" "${CMAKE_CURRENT_SOURCE_DIR}/main.py"
                   COMMAND "sh" "-c" "cp ${CMAKE_CURRENT_BINARY_DIR}/dist/main ${OUTPUT}"
                   DEPENDS ${DEPS}
                   BYPRODUCTS ${OUTPUT})


install(PROGRAMS ${OUTPUT} DESTINATION bin)

if(BUILD_DOCS)
    include("cminx")
    cminx_gen_rst("${CMAKE_CURRENT_SOURCE_DIR}/cmake/" "${CMAKE_CURRENT_SOURCE_DIR}/docs/source/developer/cmake" "cmake")

    cminx_add_docs_target("${CMAKE_CURRENT_SOURCE_DIR}/docs" "${CMAKE_CURRENT_BINARY_DIR}/docs" html)
endif()

if(BUILD_TESTING)
    message("Building tests")
    include("${PROJECT_SOURCE_DIR}/cmake/get_cpp.cmake")
    include("${PROJECT_SOURCE_DIR}/cmake/get_cmake_test.cmake")

    include(cmake_test/cmake_test)
    include(CTest)


    add_subdirectory("tests")

endif()

#Define functions and set source directory
include("cminx")
