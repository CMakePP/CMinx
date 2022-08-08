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
# Custom function to locate a Python module. Requires the Python interpreter to
# be located first.
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
        cmake_parse_arguments(
                PYMODULE "${options}" "${single_vals}" "${multi_vals}" ${ARGN}
        )

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
