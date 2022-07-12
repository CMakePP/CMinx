#!/usr/bin/python3
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

from cminx.rstwriter import RSTWriter
#from cminx.rst_validator import RSTValidator #No longer in cminx package, included in test/ directory instead as not needed for general operation

if __name__ == "__main__":

    #First we need to build an RSTWriter to validate
    writer = RSTWriter("Title")
    writer.text("This is a test")
    writer.bulleted_list("test", "No")
    writer.enumerated_list(1, "two")
    writer.doctest('print("test")', 'test')
    d = writer.directive("DANGER")
    d.text("This is john")


    #Make a table of values
    tab = [
    [0, 1, 2, 3],
    [4, 5, 6, 7],
    [8, 9, 10, 11]
    ]
    writer.simple_table(tab, column_headings=["Column 1", "Column 2", "Column 3", "Column 4"])


    #Next step is very simple. Just instantiate the validator with your desired settings and the writer
    #Then call validate()
    validator = RSTValidator(writer, werror = True)
    print(validator.validate())
