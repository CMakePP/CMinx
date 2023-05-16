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

import dataclasses


@dataclasses.dataclass
class CMakeSyntaxException(Exception):
    """
    Denotes a syntax error in the CMake source code.
    This is usually not recoverable and analysis
    of the CMake code is not guaranteed to be consistent,
    so generation of this exception is expected to
    halt the program.
    """

    msg: str
    """A message describing the syntax error."""

    line: int
    """
    The line in the CMake file where the exception was detected.
    Note that this may not be the line where the error is actually located
    in the source, only where the lexer or parser detected an error.
    """
