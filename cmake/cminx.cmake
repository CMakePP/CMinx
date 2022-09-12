# Copyright 2021 CMakePP
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
#
include_guard()

#[[[
# Generate documentation RST from source CMake files.
#
# :param dir: Directory to search for source files. Can also be a single file.
# :type dir: dir
# :param output: Directory to store output
# :type output: dir
# :param \*args: Additional parameters to forward to CMinx. Parameters are
#                forwarded verbatim.
#]]
function(cminx_gen_rst _cgd_dir _cgd_output)
    set(_cgr_cminx_options "")
    if(IS_DIRECTORY "${_cgd_dir}")
        list(APPEND _cgr_cminx_options "-r")
    endif()

    if(${ARGC} GREATER 2)
        list(APPEND _cgr_cminx_options "${ARGN}")
    endif()

    execute_process(
        COMMAND "${CMINX_EXECUTABLE}" "${_cgd_dir}" ${_cgr_cminx_options}
                "-o" "${_cgd_output}"
        OUTPUT_VARIABLE process_output
        ERROR_VARIABLE process_err
        RESULT_VARIABLE process_result
        COMMAND_ERROR_IS_FATAL ANY
    )
endfunction()
