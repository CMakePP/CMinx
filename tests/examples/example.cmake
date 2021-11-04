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
#[[
# This is a normal block comment and will not
# be treated as a doccomment.
#]]
include_guard()

#[[[
# This function has very basic documentation.
#
# This function's description stays close to idealized formatting and does not do
# anything fancy.
#
# :param person: The person this function says hi to
# :param me: What my name is
# :type person: string
# :type me: string
#]]
function(say_hi_to person me)
    message("Hi ${person}, I am ${me}")
endfunction()

#[[[
This macro says hi.
This documentation uses a differing format,
but is still processed correctly.

:param person: The person we want to greet.
:type person: string 
#]]
macro(macro_say_hi person)
   message("Hi ${person}")
endmacro()


#[[[
# This is an example of variable documentation.
# This variable is a list of string values.
#]]
set(MyList "Value" "Value 2")


#[[[
# This is another example of variable documentation.
# This variable is a string variable.
#]]
set(MyString "String")
