#!/usr/bin/python3

from cmakedoc.rstwriter import RSTWriter

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

#Johnn wants an image under his admonition
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

#Automatically rebuild header whenever title changes
writer.title = "This title is different"

#Comment below and 'with' statement are equivalent, shows that write_to_file can handle both strings and file-like objects
#writer.write_to_file("file.rst")
with open("file.rst", "w") as f:
        writer.write_to_file(f)

