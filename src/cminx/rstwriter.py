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

"""
This module and associated classes provide a pure-Python interface for generating reStructuredText.
The generated text may be either consumed by another Python application or directly written to a file-like object.
This module does not currently perform syntax validation, so it is up to the application developer to
not generate invalid RST structures.


:Author: Branden Butler
:License: Apache 2.0
"""
from enum import Enum
from typing import Any, Union, IO, List, Tuple

from cminx import Settings


class ListType(Enum):
    ENUMERATED = 0
    BULLETED = 1


def interpreted_text(role: str, text: str) -> str:
    """
    This function generates an interpreted text RST element
    from the specified text and using the specified role.
    Interpreted text may appear almost anywhere regular text can
    so making it a method of :class:`RSTWriter` would limit its functionality.


    :param role: The role of the interpreted text
    :param text: The literal text of the interpreted text
    :return: The interpreted text element as a string
    """
    return f":{role}:`{text}`"


class Paragraph(object):
    """
    Represents an RST paragraph
    """

    def __init__(self, text: str, indent: str = ""):
        self.text = text
        self.prefix = indent
        self.text_string = ""
        self.build_text_string()

    def build_text_string(self):
        """
        Populates Paragraph.text_string with the
        RST string corresponding to this paragraph
        """
        self.text_string = "\n".join(
            [self.prefix + text for text in self.text.split("\n")])

    def __str__(self):
        return self.text_string


class Field(object):
    """
    Represents an RST field, such as Author
    """

    def __init__(self, field_name: str, field_text: str, indent: str = ""):
        self.field_name = field_name
        self.field_text = field_text
        self.field_string = ""
        self.indent = indent
        self.build_field_string()

    def build_field_string(self):
        """
        Populates Field.field_string with the
        RST string corresponding to this field
        """

        self.field_string = f"\n{self.indent}:{self.field_name}: {self.field_text}"

    def __str__(self):
        return self.field_string


class DocTest(object):
    """
    Represents an RST DocTest
    """

    def __init__(self, test_line: str, expected_output: str, indent=""):
        self.test_line = test_line
        self.expected_output = expected_output
        self.doctest_string = ""
        self.indent = indent
        self.build_doctest_string()

    def build_doctest_string(self):
        """
        Populates DocTest.doctest_string with the
        RST string corresponding to this DocTest
        """
        self.doctest_string = f"\n{self.indent}>>> {self.test_line}\n{self.expected_output}\n"

    def __str__(self):
        return self.doctest_string


class RSTList(object):
    """
    Represents one of the two types of RST lists:
    Enumerated or Bulleted
    """

    def __init__(self, items: Tuple[str], list_type: ListType, indent: str = ""):
        self.items = items
        self.list_type = list_type
        self.list_string = ""
        self.indent = indent
        self.build_list_string()

    def build_list_string(self):
        """
        Populates RSTList.list_string with the
        RST string corresponding to this list
        """

        self.list_string = "\n"
        if self.list_type == ListType.ENUMERATED:
            for i in range(0, len(self.items)):
                self.list_string += f"{self.indent}{i + 1}. {self.items[i]}\n"
        elif self.list_type == ListType.BULLETED:
            for item in self.items:
                self.list_string += f"{self.indent}* {item}\n"
        else:
            raise ValueError("Unknown list type")

    def __str__(self):
        return self.list_string


class Heading(object):
    """
    Represents a section heading
    """

    def __init__(self, title: str, header_char: str):
        self.title = title
        self.header_char = header_char
        self.heading_string = ""
        self.build_heading_string()

    def build_heading_string(self):
        """
        Populates Heading.heading_string with the
        RST string corresponding to this heading
        """
        heading = ""
        for _ in self.title:
            heading += self.header_char
        self.heading_string = f"\n{heading}\n{self.title}\n{heading}"

    def __str__(self):
        return self.heading_string


class SimpleTable(object):
    """
    Represents an RST simple table.
    """

    def __init__(self, tab: List[List[str]], headings: List[str]):
        self.table = tab
        self.column_headings = headings
        self.table_string = ""
        self.build_table_string()

    def build_table_string(self):
        """
        Populates SimpleTable.table_string with the
        RST string equivalent of this table
        """
        # Easiest way to do this is loop over all cells and find the longest element, use that to compute the row
        # separator width, and then loop over cells again to add them in with proper separation. Fastest way is to
        # compute the separator width, then use list comprehension to build the table string. Probably going to be
        # much less readable. Performance differences will be minimal unless we're building tables with thousands of
        # cells.
        row_separator = ""
        row_separator_width = 0

        # Used to ensure number of columns is consistent throughout the table;
        # Length of row gives number of cells in row, which corresponds to
        # number of columns
        num_columns = len(self.table[0])

        if len(self.column_headings) != 0 and len(
                self.column_headings) != num_columns:
            raise ValueError(
                "Different number of headings than number of columns in table")

        # Find the longest cell to use as the row separator width Yes I know doing it this way is inefficient,
        # but readability is more important unless we're dealing with thousands
        # of cells.
        for row in self.table:
            # Check column number against number of cells in row; should be
            # equal
            if len(row) != num_columns:
                raise ValueError("Number of columns in table is inconsistent")
            for cell in row:
                # Temporarily cache in case calculating length is
                # time-consuming.
                cell_length = len(str(cell))
                row_separator_width = cell_length if cell_length > row_separator_width else row_separator_width

        # Account for column headings, in case they're longer than the cells
        for heading in self.column_headings:
            length = len(heading)  # Cache so only need to compute length once
            row_separator_width = length if length > row_separator_width else row_separator_width

        # We know the width, now to construct the separator itself
        for i in range(row_separator_width):
            row_separator += "="

        table_str = ""
        # Index zero is heading overline, index 1 is headings, index 2 is
        # underline
        heading_lines = ["", "", ""]
        # Build heading overlines/underlines and add correct spacing
        for heading in self.column_headings:
            heading_len = len(heading)
            for i in range(0, row_separator_width):
                heading_lines[0] += '='

                # If current line position is not greater than the length of the heading, add the character at position
                # Else, add spaces until end of row separator
                if i < heading_len:
                    heading_lines[1] += heading[i]
                else:
                    heading_lines[1] += " "
            heading_lines[0] += "  "  # Recommended 2 spaces between columns
            heading_lines[1] += "  "

        # Overline and underline should be the same
        heading_lines[2] = heading_lines[0]
        table_str += "\n".join(heading_lines) + "\n"

        # Add cells to table string
        for row in self.table:
            row_str = ""
            for cell in row:
                row_str += str(cell)
                for i in range(0, row_separator_width - len(str(cell))):
                    row_str += " "
                row_str += "  "
            table_str += row_str + "\n"
        for _ in self.table[0]:
            table_str += row_separator + "  "
        table_str += "\n"
        self.table_string = table_str

    def __str__(self):
        return self.table_string


class DirectiveHeading(object):
    """
    Represents the unique heading for a Directive (.. :<name>:)
    """

    def __init__(self, title: str, indent: str, args: str):
        self.title = title
        self.indent = indent
        self.args = args
        self.heading_string = ""
        self.build_heading_string()

    def build_heading_string(self):
        self.heading_string = f"\n{self.indent}.. {self.title}:: {self.args}"

    def __str__(self):
        return self.heading_string


class Option(object):
    """
    Represents a directive option, such as maxdepth
    """

    def __init__(self, name: str, value: str, indent: str):
        self.name = name
        self.value = value
        self.indent = indent
        self.option_string = ""
        self.build_option_string()

    def build_option_string(self):
        self.option_string = f"{self.indent}:{self.name}: {self.value}"

    def __str__(self):
        return self.option_string


def get_indents(num) -> str:
    """
    Get the string containing the necessary indent.

    :return: A string containing the correct number of whitespace characters, derived from the indent level.
    """
    indents = ""
    for i in range(0, num):
        # Directives require the first non-whitespace character of every line to line up with the first letter of
        # the directive name
        indents += '   '
    return indents


class RSTWriter(object):
    """
    Base reStructuredText writer. Does not perform verification.
    This class presents an object-oriented and procedural API
    for generating reStructuredText documents. The document is
    held in an intermediate object-oriented representation until
    the text representation is requested either through
    :py:meth:`~cminx.rstwriter.RSTWriter.to_text`
    or by calling :py:func:`str` on this object.
    """

    heading_level_chars = ['#', '*', '=', '-', '_', '~', '!', '&', '@', '^']
    """Characters to use as heading overline/underline, indexed by section_level"""

    def __init__(
            self,
            title: str,
            section_level: int = 0,
            settings=Settings(), indent: int = 0):
        self.__title: str = title
        self.section_level: int = section_level
        self.settings = settings
        if settings.rst.headers is not None:
            self.heading_level_chars = settings.rst.headers

        self.indent = indent
        self.header_char: str = self.heading_level_chars[section_level]
        # Heading must be first in the document tree
        self.document: List[Any] = [self.build_heading()]

    def clear(self):
        """
        Clear all document tree elements (besides required heading)
        """
        del self.document[1:]

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, new_title: str):
        """
        Rebuild heading and replace the old one in the document tree whenever title is changed

        :param new_title: The new section title to be used.
        """
        self.__title = new_title
        self.document[0] = self.build_heading()

    def bulleted_list(self, *items: str):
        """
        Add a bulleted list to the document tree.

        :param items: varargs containing the desired list items.
        """

        self.document.append(RSTList(items, ListType.BULLETED, indent=get_indents(self.indent)))

    def enumerated_list(self, *items: str):
        """
        Add an enumerated list to the document tree; e.g.
            1. Item 1
            2. Item 2

        :param items: varargs containing the desired list items.
        """
        self.document.append(RSTList(items, ListType.ENUMERATED, indent=get_indents(self.indent)))

    def field(self, field_name: str, field_text: str):
        """
        Add a field, such as Author or Version, to the document tree.

        :param field_name: Name of the field being added, such as Author.

        :param field_text: Value of the field, such as the author's name.
        """
        self.document.append(Field(field_name, field_text, get_indents(self.indent)))

    def doctest(self, test_line: str, expected_output: str):
        """
        Adds a doctest segment to the document tree.
        A doctest segment appears as an interactive python session.
        The doctest Python module can then be used to scan for these segments
        and execute the test_line to ensure the output is the same.

        :param test_line: Python code segment being used as the line to be tested.

        :param expected_output: The exact string that is expected to be returned when test_line is evaluated.
        """
        self.document.append(DocTest(test_line, expected_output, indent=get_indents(self.indent)))

    def section(self, title: str) -> 'RSTWriter':
        """
        Constructs another RSTWriter and adds it to the document before returning it for use

        :param title: The heading title to be used for the new subsection.
        """
        sect = RSTWriter(
            title,
            section_level=self.section_level + 1,
            settings=self.settings)
        self.document.append(sect)
        return sect

    def text(self, txt: str):
        """
        Add a paragraph to document tree.

        :param txt: The content of the new paragraph.
        """
        self.document.append(Paragraph(txt, indent=get_indents(self.indent)))

    def directive(self, name: str, *arguments: str) -> 'Directive':
        """
        Construct a directive and return it

        :param name: Name of the directive being used, such as toctree or admonition.

        :param arguments: Varargs to be used as the directive arguments, such as a topic title.
        """
        w = Directive(name, self.indent, *arguments, settings=self.settings)
        self.document.append(w)
        return w

    def build_heading(self) -> Heading:
        """
        Adds overline and underline to RSTWriter.title (character is RSTWriter.header_char) and returns it

        :return: A fully constructed Heading object.
        """
        return Heading(self.__title, self.header_char)

    def simple_table(self, tab: List[List[str]], column_headings: List[str] = ()):
        """
        Add a simple table to the document tree. tab is a 2-dimensional list containing the table data. The first
        index is the row, the second is column. The first column may not contain multiple lines, all other columns
        may. column_headings is a list where each element is treated as a heading for that specific column,
        i.e. index 0 will be the heading for the leftmost column.

        :param tab: A two-dimensional list representing table data. First index is row, second is column. Each row
        must have the same number of columns.

        :param column_headings: A single-dimensional list containing column headings, if required. Index zero is the
        heading for the left-most column. List must be same length as number of columns.

        :raise ValueError: If tab has inconsistent numbers of columns or column_headings length (if nonzero) does not
        match number of columns in tab.
        """

        self.document.append(SimpleTable(tab, column_headings))

    def to_text(self) -> str:
        """
        Return text representation of this document

        :return: The completed RST document in string form.
        """
        document_string = ""
        for element in self.document:
            document_string += f"{element}\n"
        return document_string

    def __str__(self):
        """
        Equivalent to :func: `~cminx.RSTWriter.to_text`

        :return: The completed RST document in string form.
        """
        return self.to_text()

    def write_to_file(self, file: Union[str, IO]):
        """
        Write text representation of this document to file. File may be a string (path will be opened in write mode)
        or a file-like object.

        :param file: File to write to. May be a string representing a real filepath on the local filesystem (will be
        overwritten), or a file-like object.

        :raise ValueError: If file is nothing or empty string.

        :raise TypeError: If file is not str or object with 'write()' method
        """

        # Don't use 'is' to compare to empty string, file might be subclass of str or could be a C-built string,
        # both of which are different references Don't use "==" to compare to None, None will be a singleton in every
        # case and objects may override __eq__()
        if file == "" or file is None:
            raise ValueError("File not set, cannot write RST document")
        if isinstance(file, str):
            # Strip leading/trailing whitespace, so we don't end up with '. '
            # as a file, I have seen it happen before
            with open(file.strip(),
                      'w') as f:
                f.write(str(self))
        else:
            # Might be invalid object, checking to make sure it's file-like
            if hasattr(file, "write"):
                file.write(str(self))
            else:
                # Not file-like object or string
                raise TypeError(
                    f"File is neither a string nor a file-like object, type is {type(file)}, cannot write RST document")


class Directive(RSTWriter):
    """
    Use :func:`cminx.RSTWriter.directive` to construct.
    Represents an RST directive, such as toctree or an admonition.
    Does not verify that the directive or its arguments are valid.
    """

    def __init__(self, name: str, indent: int = 0, *arguments: str, settings: Settings = Settings()):
        """
        :param name: Name of the directive being constructed, eg. toctree or admonition.

        :param indent: Indent level of this directive. 0 is root, 1 is under another directive, etc.

        :param arguments: Varargs to be used as the directive arguments, eg. a topic's title.
        """

        self.arguments = arguments
        self.options = []
        super().__init__(name, settings=settings, indent=indent + 1)

    def build_heading(self) -> DirectiveHeading:
        """
        Build directive heading format (ex. '.. toctree::') and return.

        :return: Correctly formatted directive heading string.
        """
        return DirectiveHeading(
            self.title, get_indents(
                self.indent - 1), self.format_arguments())

    def format_arguments(self) -> str:
        """
        Format argument list into the correct argument string for use with directives.

        :return: A string representing the directive arguments.
        """
        return ','.join(map(str, self.arguments))

    def option(self, name: str, value: str = ""):
        """
        Add an option, such as toctree's maxdepth. Does not verify if valid option
        """
        self.options.append(
            Option(
                name,
                value,
                get_indents(
                    self.indent)))

    def to_text(self) -> str:
        """
        Return text representation of this document

        :return: The completed RST document in string form.
        """
        document_string = f"{self.document[0]}\n"

        for option in self.options:
            document_string += f"{option}\n"

        if len(self.document) > 1:
            document_string += "\n"

        for element in self.document[1:]:
            document_string += f"{element}\n"
        return document_string
