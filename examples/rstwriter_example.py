#!/usr/bin/python3

from cmakedoc.rstwriter import RSTWriter

writer = RSTWriter("This is a test")
writer.field("Author", "Branden Butler")
writer.text("Text")
writer.doctest(r"print('test')", r"test")
d = writer.directive("admonition", "John")
d.text("Social network")
#d.option('maxdepth', 2)
#d.text('file/to/include')
img = d.directive("image", "image.png")
img.option("width", 500)
img.option("height", 100)
s = writer.section('A subsection')
s.text("Subsection's content")
s.bulleted_list("Item 1", "Item 2", "Item 3")
s.enumerated_list("Item 1", "Item 2", "Item 3")
writer.title = "This title is different" #Automatically rebuild header whenever title changes


#writer.write_to_file("file.rst")
with open("file.rst", "w") as f: #Equivalent to above commented line, shows that both work the same
        writer.write_to_file(f)

