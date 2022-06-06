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

#[[
# This function encapsulates the process of getting CMakePP using CMake's
# FetchContent module. We have encapsulated it in a function so we can set
# the options for its configure step without affecting the options for the
# parent project's configure step (namely we do not want to build CMakePP's
# unit tests).
#]]
macro(get_cpp)
    include(cpp/cpp OPTIONAL RESULT_VARIABLE cpp_found)
    if(NOT cpp_found)



        # Store whether we are building tests or not, then turn off the tests
        set(build_testing_old "${BUILD_TESTING}")
        set(BUILD_TESTING OFF CACHE BOOL "" FORCE)
        # Download CMakePP and bring it into scope
        include(FetchContent)
        FetchContent_Declare(
             cpp
             GIT_REPOSITORY https://github.com/CMakePP/CMakePackagingProject
       )
       FetchContent_MakeAvailable(cpp)

       # Restore the previous value
       set(BUILD_TESTING "${build_testing_old}" CACHE BOOL "" FORCE)
    endif()
endmacro()

# Call the function we just wrote to get CMakePP
get_cpp()

# Include CMakePP
include(cpp/cpp)
