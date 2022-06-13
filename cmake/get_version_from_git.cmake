# Copyright 2022 CMakePP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

include_guard()

#[[[
# Uses Git to determine the version of a git repo.
#
# :param gvfg_result: The variable name to assign the result to.
# :param gvfg_git_root: The directory containing the .git/ directory.
#
# Example:
#
# get_version_from_git(MY_PROJECT_VERSION ${CMAKE_CURRENT_SOURCE_DIR})
# message("My project's version is: ${MY_PROJECT_VERSION}")
#]]
function(get_version_from_git gvfg_result gvfg_git_root)
    find_package(Git QUIET REQUIRED)

    # Invoke git command to get the tag
    execute_process(COMMAND ${GIT_EXECUTABLE} describe --tags --abbrev=0
                    WORKING_DIRECTORY ${gvfg_git_root}
                    OUTPUT_VARIABLE gvfg_version
                    OUTPUT_STRIP_TRAILING_WHITESPACE
    )

    # Remove the "v" prefix, since CMake chokes on it
    STRING(REGEX REPLACE "^v" "" gvfg_version ${gvfg_version})

    set(${gvfg_result} ${gvfg_version} PARENT_SCOPE)
endfunction()
