from cmakedoc.rstwriter import RSTWriter

from docutils.nodes import *
import docutils.parsers.rst
import docutils.utils
import docutils.frontend

def parse_rst(text: str) -> docutils.nodes.document:
    parser = docutils.parsers.rst.Parser()
    components = (docutils.parsers.rst.Parser,)
    settings = docutils.frontend.OptionParser(components=components).get_default_values()
    document = docutils.utils.new_document('<rst-doc>', settings=settings)
    parser.parse(text, document)
    return document



def process_element(element):
    mapping[type(element)](element)

def process_paragraph(p):
    print(p.astext())

def process_bullet_list(b):
    l = [element.astext() for element in b]
    print(l)

def process_table(t):
    grouping = t[0]
    body_index = grouping.first_child_matching_class(tbody)
    body = grouping[body_index]
    for row in body:
        for cell in row:
           print(cell.astext())
def process_sect(section):
    sect_title = section[0]
    print(sect_title.astext())
    for element in section[1:]:
        process_element(element)


mapping = {
    paragraph: process_paragraph,
    section: process_sect,
    bullet_list: process_bullet_list,
    table: process_table
}




if __name__ == "__main__":
    writer = RSTWriter("Title")
    writer.text("This is a test")
    writer.bulleted_list(*["test", "No"])
    #Make a table of values
    tab = [
    [0, 1, 2, 3],
    [4, 5, 6, 7],
    [8, 9, 10, 11]
    ]
    writer.simple_table(tab, column_headings=["Column 1", "Column 2", "Column 3", "Column 4"])


    txt = writer.to_text()
    doc = parse_rst(txt)
    #Begin processing at the main section
    process_element(doc[0])
