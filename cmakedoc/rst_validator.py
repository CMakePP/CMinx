#!/usr/bin/python3
from cmakedoc.rstwriter import RSTWriter

from docutils.nodes import *
import docutils.parsers.rst
import docutils.utils
import docutils.frontend

class ValidationError(RuntimeError):
    """
    Raised when something seriously wrong happens when validating RST structures.
    Situations in which this exception will be raised include:

    1. No processor mapping found for a particular RST element
    2. A 'severe' level message occurs somewhere in the RST document tree
    3. The parsed section and the RSTWriter section have two different lengths
    """
    pass

class RSTValidator:
    """
    Validates an RSTWriter document by feeding it through DocUtils and making sure everything comes out the same.
    This has the disadvantage of being unable to validate structures unsupported by DocUtils, such as toctree,
    but it works for testing to make sure RSTWriter outputs correct syntax.
    """

    def __init__(self, writer: RSTWriter, werror=False):
        """
        :param writer: RSTWriter that will be validated.

        :param werror: Whether DocUtils warnings should be treated as a failed validation.
        """
        self.mapping = {
            paragraph: self.process_paragraph,
            section: self.process_sect,
            bullet_list: self.process_list,
            enumerated_list: self.process_list,
            table: self.process_table,
            system_message: self.process_message,
            doctest_block: self.process_doctest,
            Admonition: self.process_admonition
        }
        self.writer = writer
        self.parser = docutils.parsers.rst.Parser()
        self.validated = False
        self.werror = werror

    def validate(self) -> bool:
        """
        Parse the RSTWriter text and process the document tree. Previous validated result will be wiped.
        This method may take awhile to run if validating larger documents, so cache the result if necessary.

        :return: Whether the supplied RSTWriter succeeded in being validated.

        :raises ValidationError: If validation encounters an unrecoverable or severe problem.
        """

        self.validated = True #Assume everything works until something fails down the line
        doc = self.parse_rst(self.writer.to_text())
        self.process_element(doc[0], self.writer.document)
        for msg in doc.parse_messages:
            self.process_message(msg)
        return self.validated

    def parse_rst(self, text: str) -> docutils.nodes.document:
        """
        Parse the RST text into a DocUtils document, using the RST parser

        :param text: String containing RST document to be parsed
        """

        components = (docutils.parsers.rst.Parser,)
        settings = docutils.frontend.OptionParser(components=components).get_default_values()
        document = docutils.utils.new_document('<rst-doc>', settings=settings)
        self.parser.parse(text, document)
        return document


    def process_message(self, msg: system_message):
         """
         Processes all DocUtils messages found in the document tree, as well as those found in the parse_messages list.
         If the level is error and higher, or warning and higher if werror is True, then the validation status is set to False.

         :param msg: DocUtils message node to be processed

         :raises ValidationError: If message's level is severe
         """

         level = msg['level']
         if level >= (2 if self.werror else 3): #Warn or higher if werror, else only error or higher
              self.validated = False
         if level >= 3: #Severe, we need to raise a stink about this
              raise ValidationError(msg)

    def process_element(self, element, to_validate):
        """
        All elements in the document first pass through here.
        The specific processor is found by matching the list of superclasses
        against RSTValidator.mapping in order of method resolution.

        :param element: DocUtils document element, the processor used is found by matching element's class and superclasses.

        :param to_validate: RSTWriter element being validated, should match the DocUtils equivalent

        :raises ValidationError: If the processor used raises it or a processor could not be found.
        """
        for t in type(element).mro(): #Look up the chain of superclasses until we find a mapping, in method resolution order
            if t in self.mapping:
                self.mapping[t](element, to_validate)
                break
        else: #For-else clause, executes if break is not called
            raise ValidationError(f"No processor mapping found for {type(element)}")

    def process_paragraph(self, para: paragraph, to_validate):
        """
        Processor for the paragraph element.

        :param para: DocUtils paragraph element to validate against.

        :param to_validate: RSTWriter Paragraph element to be validated.
        """
        if para.astext() != to_validate.text:
            self.validated = False

    def process_list(self, rst_list, to_validate):
        """
        Processor for list elements, both bulleted and enumerated.

        :param rst_list: DocUtils list element to validate against.

        :param to_validate: RSTWriter List element to validate.
        """
        for i in range(0, len(rst_list)):
            if rst_list[i].astext() != str(to_validate.items[i]):
                self.validated = False

    def process_admonition(self, ad: Admonition, to_validate):
        """
        Processor for admonitions, handles all types including general, warning, danger, etc.

        :param ad: DocUtils Admonition element, may be of any subclass

        :param to_validate: RSTWriter Directive element to validate. RSTWriter makes no distinction against types of directives.
        """

        if ad[0].astext() != to_validate.document[1].text:
            self.validated = False

    def process_doctest(self, doctest, to_validate):
        """
        Processor for DocTest elements. DocUtils does not store the test_line
        and expected_output separately, so string processing is needed. The triple chevrons
        are removed via a str.lsplit() call, the expected_output is unaltered.

        :param doctest: DocUtils doctest_block element to validate against.

        :param to_validate: RSTWriter DocTest element to validate.
        """
        parts = doctest[0].split('\n')
        test_line = parts[0].lstrip("> ")
        expected_output = "\n".join(parts[1:])
        if test_line != to_validate.test_line or expected_output != to_validate.expected_output:
            self.validated = False

    def process_table(self, t, to_validate):
        """
        Processor for Table elements. DocUtils makes no distinction between simple
        tables and grid tables, this processor can only handle simple tables.

        :param t: DocUtils table element to validate against.

        :param to_validate: RSTWriter SimpleTable element to validate.
        """

        grouping = t[0]
        body_index = grouping.first_child_matching_class(tbody)
        body = grouping[body_index]
        for i in range(0, len(body)):
           for j in range(0, len(body[i])):
               if body[i][j].astext() != str(to_validate.table[i][j]):
                   self.validated = False

    def process_sect(self, section, to_validate):
        """
        Processor for Section elements. Filters out system_message elements and dispatches them
        to their processor before looping over all subelements in the section.

        :param section: DocUtils section element containing subelements and possibly system messages, each element will be processed separately.

        :param to_validate: RSTWriter document list to validate.

        :raises ValidationError: If any subelements do or the two document trees do not have the same length.
        """

        sect_title = section[0]
        if sect_title.astext() != to_validate[0].title:
            self.validated = False

        section_cleaned = list(filter(self.is_not_message, section)) #Remove all messages and process them before processing rest of the document
        if len(section_cleaned) != len(to_validate): #Our two documents are different lengths
            raise ValidationError("Parsed section and RSTWriter section are two different lengths")

        for i in range(1, len(section_cleaned)): #Section and to_validate should now have the same number of elements
            self.process_element(section_cleaned[i], to_validate[i])

    def is_not_message(self, e) -> bool:
        """
        Determines if e is a message and if so, dispatches it to its processor.

        :param e: Element to check

        :return: True if element is a message, False otherwise
        """
        if system_message in type(e).mro():
            self.process_message(e)
            return False
        else: #Included for readability
            return True


