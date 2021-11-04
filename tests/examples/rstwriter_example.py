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

#First construct the root writer, only argument is the document title
writer = RSTWriter("This is a test")

#Next add any fields needed, such as author, copyright, or license.
writer.field("Author", "Branden Butler")

#Add a paragraph to the root section, after the fields.
writer.text("Text")

#Add a doctest for both showing usage and to ensure future revisions still work the same.
writer.doctest(r"print('test')", r"test")

#General admonition, we want people to know about John.
d = writer.directive("admonition", "John")

#John's social network
d.text("Social network")

#For other directives you may add options, such as the one below for toctree
#d.option('maxdepth', 2)
#d.text('file/to/include')

#John wants an image under his admonition
img = d.directive("image", "image.png")

#Images can also have options, here we change the image width and height, stretching it
img.option("width", 500)
img.option("height", 100)

#Adding a subsection to the root (appears after John's admonition, social network, and image)
s = writer.section('A subsection')
s.text("Subsection's content")

#Adding lists. These use varargs so if you have a prebuilt list already you'll want to splat it out
s.bulleted_list("Item 1", "Item 2", "Item 3")
s.enumerated_list("Item 1", "Item 2", "Item 3")

#Make a table of values
tab = [
[0, 1, 2, 3],
[4, 5, 6, 7],
[8, 9, 10, 11]
]
s.simple_table(tab, column_headings=["Column 1", "Column 2", "Column 3", "Column 4"])

#Automatically rebuild header whenever title changes
writer.title = "This title is different"

#Comment below and 'with' statement are equivalent, shows that write_to_file can handle both strings and file-like objects
#writer.write_to_file("file.rst")
with open("file.rst", "w") as f:
        writer.write_to_file(f)

