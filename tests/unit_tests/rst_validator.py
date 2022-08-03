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
import docutils.frontend
import docutils.parsers.rst
import docutils.utils
from docutils.nodes import paragraph, section, bullet_list, enumerated_list, table, system_message, doctest_block, \
    Admonition, field_list, image, tbody

from cminx.rstwriter import RSTWriter, Paragraph, RSTList, Field, DocTest, SimpleTable, Directive


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
    Currently supported validation targets:
    1. Sections and headings
    2. Paragraphs
    3. Both enumerated and bulleted lists
    4. Simple tables
    5. Doctests
    6. Fields
    7. Admonitions, such as DANGER. Other directive types not supported

    """

    def __init__(self, writer: RSTWriter, werror=False, doc=None):
        """
        :param writer: RSTWriter that will be validated.

        :param werror: Whether DocUtils warnings should be treated as a failed validation.

        :param doc: Optional DocUtils document to validate against. If None, a document will be generated from the output of writer
        """
        self.mapping = {
            paragraph: self.process_paragraph,
            section: self.process_sect,
            bullet_list: self.process_list,
            enumerated_list: self.process_list,
            table: self.process_table,
            system_message: self.process_message,
            doctest_block: self.process_doctest,
            Admonition: self.process_admonition,
            field_list: self.process_field_list,
            image: self.process_image
        }
        self.writer = writer
        self.parser = docutils.parsers.rst.Parser()
        self.doc = doc
        self.validated = False
        self.werror = werror
        self.failures = []

    def validate(self) -> bool:
        """
        Parse the RSTWriter text and process the document tree. Previous validated result will be wiped.
        This method may take awhile to run if validating larger documents, so cache the result if necessary.

        :return: Whether the supplied RSTWriter succeeded in being validated.

        :raises ValidationError: If validation encounters an unrecoverable or severe problem.
        """

        self.validated = True  # Assume everything works until something fails down the line
        self.failures = []
        if self.doc is None:
            self.doc = RSTValidator.parse_rst(self.parser,
                                              self.writer.to_text())
        self.process_element(self.doc[0], self.writer)
        for msg in self.doc.parse_messages:
            self.process_message(msg)
        return self.validated

    def fail(self, msg):
        """
        Record a validation failure

        :param msg: A string saying what happened that caused a failed validation
        """

        self.failures.append(msg)
        self.validated = False

    @staticmethod
    def parse_rst(parser, text: str) -> docutils.nodes.document:
        """
        Parse the RST text into a DocUtils document, using the RST parser

        :param text: String containing RST document to be parsed
        """

        components = (docutils.parsers.rst.Parser,)
        settings = docutils.frontend.OptionParser(
            components=components).get_default_values()
        document = docutils.utils.new_document('<rst-doc>', settings=settings)
        parser.parse(text, document)
        return document

    def process_message(self, msg: system_message):
        """
         Processes all DocUtils messages found in the document tree, as well as those found in the parse_messages list.
         If the level is error and higher, or warning and higher if werror is True, then the validation status is set to False.

         :param msg: DocUtils message node to be processed

         :raises ValidationError: If message's level is severe
         """

        level = msg['level']
        if level >= (2 if self.werror else
        3):  # Warn or higher if werror, else only error or higher
            self.fail(msg)
        if level >= 3:  # Severe, we need to raise a stink about this
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
        for t in type(element).mro(
        ):  # Look up the chain of superclasses until we find a mapping, in method resolution order
            if t in self.mapping:
                self.mapping[t](element, to_validate)
                break
        else:  # For-else clause, executes if break is not called
            raise ValidationError(
                f"No processor mapping found for {type(element)}")

    def process_paragraph(self, para: paragraph, to_validate: Paragraph):
        """
        Processor for the paragraph element.

        :param para: DocUtils paragraph element to validate against.

        :param to_validate: RSTWriter Paragraph element to be validated.
        """
        if para.astext() != to_validate.text:
            self.fail(
                f"Parsed paragraph {para.astext()} != original paragraph {to_validate.text}"
            )

    def process_field_list(self, fields: field_list, to_validate: Field):
        """
        Processor for field lists

        :param fields: DocUtils field_list element to validate against

        :param to_validate): RSTWriter Field element to validate
        """

        name = fields[0][0].astext()
        text = fields[0][1].astext()
        if name != to_validate.field_name:
            self.fail(
                f"Parsed field name '{name}' != original field name '{to_validate.field_name}'"
            )

        if text != to_validate.field_text:
            self.fail(
                f"Parsed field text {text} != original field text '{to_validate.field_text}'"
            )

    def process_list(self, rst_list, to_validate: RSTList):
        """
        Processor for list elements, both bulleted and enumerated.

        :param rst_list: DocUtils list element to validate against.

        :param to_validate: RSTWriter List element to validate.
        """
        for i in range(0, len(rst_list)):
            if rst_list[i].astext() != str(to_validate.items[i]):
                self.fail("Parsed list items do now match original list items")

    def process_admonition(self, ad: Admonition, to_validate: Directive):
        """
        Processor for admonitions, handles all types including general, warning, danger, etc.

        :param ad: DocUtils Admonition element, may be of any subclass

        :param to_validate: RSTWriter Directive element to validate. RSTWriter makes no distinction against types of directives.
        """

        if ad[0].astext() != to_validate.document[1].text:
            self.fail(
                f"Parsed admonition text ({ad[0].astext()}) does not match original admonition text ({to_validate.document[1].text}"
            )

    def process_image(self, img: image, to_validate: Directive):
        """
        Processor for image directives. DocUtils does not have a Directive
        superclass, so even though this method could process all directives
        there is no way to set this as a processor for all of them.

        :param img: DocUtils image element to validate against

        :param to_validate: RSTWriter Directive element to validate. RSTWriter makes no distinction against types of directives.

        :raises ValidationError: If there is an option present in to_validate but not in img
        """
        for option in to_validate.options:
            if option.name in img:
                if str(option.value) != str(img[option.name]):
                    self.fail(
                        "Parsed option values do not match original option values"
                    )
            else:
                raise ValidationError(
                    f"Option {option.name} not in parsed document")

    def process_doctest(self, doctest: doctest_block, to_validate: DocTest):
        """
        Processor for DocTest elements. DocUtils does not store the test_line
        and expected_output separately, so string processing is needed. The triple chevrons
        are removed via a str.lstrip() call, the expected_output is unaltered.

        :param doctest: DocUtils doctest_block element to validate against.

        :param to_validate: RSTWriter DocTest element to validate.
        """
        parts = doctest[0].split('\n')
        test_line = parts[0].lstrip("> ")
        expected_output = "\n".join(parts[1:])
        if test_line != to_validate.test_line or expected_output != to_validate.expected_output:
            self.fail(
                "Parsed test line or expected output do not match either of the original values"
            )

    def process_table(self, t: table, to_validate: SimpleTable):
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
                    self.fail(
                        "Parsed table values do not match original table values"
                    )

    def process_sect(self, sect: section, to_validate: RSTWriter):
        """
        Processor for Section elements. Filters out system_message elements and dispatches them
        to their processor before looping over all subelements in the section.

        :param sect: DocUtils section element containing subelements and possibly system messages, each element will be processed separately.

        :param to_validate: RSTWriter document list to validate.

        :raises ValidationError: If any subelements do or the two document trees do not have the same length.
        """
        sect_title = sect[0]
        if sect_title.astext() != to_validate.document[0].title:
            self.fail(
                f"Parsed section title '{sect_title.astext()}' does not match original section title '{to_validate.document[0].title}'"
            )

        section_cleaned = list(
            filter(self.is_not_message, sect)
        )  # Remove all messages and process them before processing rest of the document
        if len(section_cleaned) != len(
                to_validate.document
        ):  # Our two documents are different lengths
            raise ValidationError([
                "Parsed section and RSTWriter section are two different lengths",
                str(section_cleaned),
                str(to_validate.document)
            ])

        for i in range(
                1, len(section_cleaned)
        ):  # Section and to_validate should now have the same number of elements
            self.process_element(section_cleaned[i], to_validate.document[i])

    def is_not_message(self, e) -> bool:
        """
        Determines if e is a message and if so, dispatches it to its processor.

        :param e: Element to check

        :return: True if element is a message, False otherwise
        """
        if system_message in type(e).mro():
            self.process_message(e)
            return False
        else:  # Included for readability
            return True
