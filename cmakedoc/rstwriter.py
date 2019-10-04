#!/usr/bin/python3

"""
This module and associated classes provide a pure-Python interface for generating reStructuredText.
The generated text may be either consumed by another Python application or directly written to a file-like object.
This module does not currently perform syntax validation so it is up to the application developer to
not generate invalid invalid RST structures.


:Author: Branden Butler
:License: Apache 2.0
"""

class RSTWriter(object):
	"""
	Base reStructuredText writer. Does not perform verification.
	"""

	heading_level_chars = ['#', '*', '=', '-', '_', '~', '!', '&', '@', '^']
	"""Characters to use as heading overline/underline, indexed by section_level"""



	def __init__(self, title: str, header_char: str = "#", section_level: int = 0):
		self.__title: str = title
		self.header_char: str = header_char
		self.section_level: int = section_level
		self.document = [self.build_heading()] #Heading must be first in the document tree

	@property
	def title(self):
		return self.__title

	@title.setter
	def title(self, new_title):
		"""Rebuild heading and replace the old one in the document tree whenever title is changed"""
		self.__title = new_title
		self.document[0] = self.build_heading()

	def bulleted_list(self, *items):
		"""Add a bulleted list to the document tree."""
		list_string = "\n"
		for item in items:
			list_string += f"* {item}\n"
		self.document.append(list_string)

	def enumerated_list(self, *items):
		"""
		Add an enumerated list to the document tree; e.g.
			1. Item 1
			2. Item 2

		:param items: varargs containing the desired list items.
		"""
		list_string = "\n"
		for i in range(0, len(items)):
			list_string += f"{i + 1}. {items[i]}\n"
		self.document.append(list_string)

	def field(self, field_name: str, field_text: str):
		"""
		Add a field, such as Author or Version, to the document tree.

		:param fieldname: Name of the field being added, such as Author.

		:param field_text: Value of the field, such as the author's name.
		"""
		self.document.append(f":{field_name}: {field_text}")


	def doctest(self, test_line: str, expected_output: str):
		"""
		Adds a doctest segment to the document tree.
		A doctest segment appears as an interactive python session.
		The doctest Python module can then be used to scan for these segments
		and execute the test_line to ensure the output is the same.

		:param test_line: Python code segment being used as the line to be tested.

		:param expected_output: The exact string that is expected to be returned when test_line is evaluated.
		"""
		self.document.append(f"\n>>> {test_line}\n{expected_output}\n")

	def section(self, title: str):
		"""
		Constructs another RSTWriter and adds it to the document before returning it for use

		:param title: The heading title to be used for the new subsection.
		"""
		sect = RSTWriter(title, header_char = self.heading_level_chars[self.section_level + 1], section_level = self.section_level + 1)
		self.document.append(sect)
		return sect

	def text(self, txt: str):
		"""
		Add a paragraph to document tree.

		:param txt: The content of the new paragraph.
		"""
		self.document.append(f"\n{txt}")

	def directive(self, name, *arguments):
		"""
		Construct a directive and return it

		:param name: Name of the directive being used, such as toctree or admonition.

		:param arguments: Varargs to be used as the directive arguments, such as a topic title.
		"""
		w = Directive(name, 0, *arguments)
		self.document.append(w)
		return w

	def build_heading(self):
		"""
		Adds overline and underline to RSTWriter.title (character is RSTWriter.header_char) and returns it

		:return: The formatted heading string.
		"""
		heading = ""
		for i in self.__title:
			heading += self.header_char
		return f"\n{heading}\n{self.__title}\n{heading}"


	def to_text(self):
		"""
		Return text representation of this document

		:return: The completed RST document in string form.
		"""
		document_string = ""
		for element in self.document:
			document_string += f"{element}\n"
		return document_string

	def __str__(self):
		return self.to_text()

	def write_to_file(self, file):
		"""
		Write text representation of this document to file. File may be a string (path will be opened in write mode) or a file-like object.

		:param file: File to write to. May be a string representing a real filepath on the local filesystem (will be overwritten), or a file-like object.

		:raise ValueError: If file is nothing or empty string.

		:raise TypeError: If file is not str or object with 'write()' method
		"""

		if file == "" or file is None: #Don't use 'is' to compare to empty string, file might be subclass of str or could be a C-built string, both of which are different references
			raise ValueError("File not set, cannot write RST document")
		if isinstance(file, str):
			with open(file.strip(), 'w') as f: #Strip leading/trailing whitespace so we don't end up with '. ' as a file, I have seen it happen before
				f.write(str(self))
		else:
			#Might be invalid object, checking to make sure it's file-like
			if hasattr(file, "write"):
				file.write(str(self))
			else:
				#Not file-like object or string
				raise TypeError(f"File is neither a string nor a file-like object, type is {type(file)}, cannot write RST document")

class Directive(RSTWriter):
	"""
	Use :func:`cmakedoc.RSTWriter.directive` to construct.
	Represents an RST directive, such as toctree or an admonition.
	Does not verify that the directive or its arguments are valid.
	"""

	def __init__(self, name, indent=0, *arguments):
		self.indent: int = indent
		self.arguments = arguments
		super().__init__(name)

	def directive(self, title, *arguments):
		"""Add a sub-directive"""
		d = Directive(title, self.indent + 1, *arguments)
		self.document.append(d)
		return d

	def build_heading(self):
		"""
		Build directive heading format (ex. '.. toctree::') and return
		"""
		return f"\n{self.get_indents(self.indent)}.. {self.title}:: {self.format_arguments()}"

	def format_arguments(self):
		return ','.join(map(str, self.arguments))

	def option(self, name: str, value=""):
		"""
		Add an option, such as toctree's maxdepth. Does not verify if valid option
		"""
		self.document.append(f"{self.get_indents(self.indent+1)}:{name}: {value}")

	def get_indents(self, num):
		"""
		Get the string containing the necessary indent
		"""
		indents = ""
		for i in range(0, num):
			indents += '   ' #Directives require the first non-whitespace character of every line to line up with the first letter of the directive name
		return indents

	def text(self, txt):
		"""
		Add paragraph to document tree, adds proper indenting for directives as well
		"""
		self.document.append(f"\n{self.get_indents(self.indent + 1)}{txt}")


