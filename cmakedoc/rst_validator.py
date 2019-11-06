#!/usr/bin/python3
from cmakedoc.rstwriter import RSTWriter

from docutils.nodes import *
import docutils.parsers.rst
import docutils.utils
import docutils.frontend

class ValidationError(RuntimeError):
    pass

class RSTValidator:
    def __init__(self, writer: RSTWriter, werror=False):
        self.mapping = {
            paragraph: self.process_paragraph,
            section: self.process_sect,
            bullet_list: self.process_bullet_list,
            table: self.process_table,
            system_message: self.process_message
        }
        self.writer = writer
        self.parser = docutils.parsers.rst.Parser()
        self.validated = False
        self.werror = werror

    def validate(self):
        self.validated = True #Assume everything works until something fails down the line
        doc = self.parse_rst(self.writer.to_text())
        self.process_element(doc[0], self.writer.document)
        for msg in doc.parse_messages:
            self.process_message(msg)
        return self.validated

    def parse_rst(self, text: str) -> docutils.nodes.document:
        components = (docutils.parsers.rst.Parser,)
        settings = docutils.frontend.OptionParser(components=components).get_default_values()
        document = docutils.utils.new_document('<rst-doc>', settings=settings)
        self.parser.parse(text, document)
        return document


    def process_message(self, msg):
         level = msg['level']
         #print(msg)
         if level >= (2 if self.werror else 3): #Warn or higher if werror, else only error or higher
              self.validated = False
         if level >= 3: #Severe, we need to raise a stink about this
              raise ValidationError(msg)

    def process_element(self, element, to_validate):
        self.mapping[type(element)](element, to_validate)

    def process_paragraph(self, p, to_validate):
        print(p.astext().strip() == to_validate.strip())

    def process_bullet_list(self, b, to_validate):
        l = [element.astext() for element in b]
        print(l)

    def process_table(self, t, to_validate):
        grouping = t[0]
        body_index = grouping.first_child_matching_class(tbody)
        body = grouping[body_index]
        for row in body:
           for cell in row:
               print(cell.astext())

    def process_sect(self, section, to_validate):
        sect_title = section[0]
        print(sect_title.astext())
        print(to_validate[0])
        for i in range(1, len(section)):
            self.process_element(section[i], to_validate[i])





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

    validator = RSTValidator(writer, werror = True)
    print(validator.validate())
    #txt = writer.to_text()
    #doc = parse_rst(txt)
    #Begin processing at the main section
    #process_element(doc[0])
