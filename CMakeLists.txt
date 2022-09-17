cmake_minimum_required(VERSION 3.19) #For Python3 recognizing version
find_package(Python3 3.8 COMPONENTS Interpreter REQUIRED)
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")

include(get_version_from_git)
get_version_from_git(CMINX_VERSION ${CMAKE_CURRENT_SOURCE_DIR})

#N.B. Not using a compiled language, by not setting we remove compiler checks
project(
    cminx
    DESCRIPTION "CMake automatic documentation generator"
    LANGUAGES NONE
    VERSION ${CMINX_VERSION}
)

option(BUILD_TESTING "Whether tests should be built ad ctest configured" OFF)

################################################################################
# Work out install paths
################################################################################
# Path, relative to install root, where binaries go
set(CMINX_BIN_DIR "bin")

# Path, relative to install root, where libraries go
set(CMINX_LIB_DIR "lib/cminx")

# Path, relative to install root, where CMake modules and config files go
set(CMINX_CMAKE_DIR "${CMINX_LIB_DIR}/cmake")

# During the configuration, building, and testing phases we use a staging
# directory as the install root. The install phase simply copies the staging
# directory to the install location. This is the absolute path of the staging
# directory.
set(CMINX_STAGE_DIR "${CMAKE_CURRENT_BINARY_DIR}/stage")

################################################################################
# Install Dependencies
################################################################################


include(python_virt_env)

# Points to the location of the build virtual environment.
set(CMINX_VENV "${CMAKE_CURRENT_BINARY_DIR}/virtual-env")

make_python_venv("${Python3_EXECUTABLE}" "${CMINX_VENV}")
python_venv_pip_install("${CMINX_VENV}" "pyinstaller")
python_venv_pip_install("${CMINX_VENV}" "wheel")
python_venv_pip_install("${CMINX_VENV}" "-e" "${CMAKE_CURRENT_SOURCE_DIR}")

################################################################################
# Build CMinx
################################################################################

set(CMINX_SRC_DIR ${CMAKE_CURRENT_SOURCE_DIR}/src/cminx)
set(CMINX_CONFIG_FILE ${CMINX_SRC_DIR}/config_default.yaml)
# N.B. this runs during configure so CMinx can be used downstream
# via fetch content
execute_process(
    COMMAND ${CMINX_VENV}/bin/python3 "-m" "PyInstaller"
                                      "--collect-data" "src/cminx"
                                      "--add-data" "${CMINX_CONFIG_FILE}:cminx"
                                      "--name" "cminx"
                                      "--onefile"
                                      "${CMAKE_CURRENT_SOURCE_DIR}/src/main.py"
    WORKING_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}"
    COMMAND_ERROR_IS_FATAL ANY
)

# Move CMinx (and the CMinx CMake module) to the stage directory
file(
    COPY ${CMAKE_CURRENT_BINARY_DIR}/dist/cminx
    DESTINATION ${CMINX_STAGE_DIR}/${CMINX_BIN_DIR}
)
file(
    COPY ${CMAKE_CURRENT_LIST_DIR}/cmake/cminx.cmake
    DESTINATION ${CMINX_STAGE_DIR}/${CMINX_CMAKE_DIR}
)

################################################################################
# Write package config files
################################################################################

include(CMakePackageConfigHelpers)
configure_package_config_file(
    "${CMAKE_CURRENT_LIST_DIR}/cmake/templates/cminx-config.cmake.in"
    "${CMINX_STAGE_DIR}/${CMINX_CMAKE_DIR}/cminx-config.cmake"
    INSTALL_DESTINATION "${CMINX_CMAKE_DIR}"
    PATH_VARS CMINX_BIN_DIR CMINX_CMAKE_DIR
)

write_basic_package_version_file(
    "${CMINX_STAGE_DIR}/${CMINX_CMAKE_DIR}/cminx-config-version.cmake"
    COMPATIBILITY AnyNewerVersion
)

################################################################################
# Testing
################################################################################

if(BUILD_TESTING)
    message("Building tests")
    include("${PROJECT_SOURCE_DIR}/cmake/get_cpp.cmake")
    include("${PROJECT_SOURCE_DIR}/cmake/get_cmake_test.cmake")

    python_venv_pip_install(${CMINX_VENV} "-e" ".[testing]")

    include(cmake_test/cmake_test)
    include(CTest)

    add_subdirectory("tests")

endif()

################################################################################
# Installation
################################################################################

install(
    DIRECTORY ${CMINX_STAGE_DIR}/
    DESTINATION ${CMAKE_INSTALL_PREFIX}
    USE_SOURCE_PERMISSIONS
)

# For fetch content purposes we make cminx_gen_rst available to the caller
find_package(cminx REQUIRED CONFIG HINTS ${CMINX_STAGE_DIR})
