#!/usr/bin/python3

import context
from cmakedoc.rstwriter import RSTWriter
from rst_validator import RSTValidator
import unittest
import os

class TestRSTWriter(unittest.TestCase):
	def setUp(self):
		self.writer = RSTWriter("Testing RSTWriter")
		self.validator = RSTValidator(self.writer, werror = True) #Treat all warnings as validation failure
		self.file = "writer_test.rst"

	def tearDown(self):
		try:
			os.remove(self.file)
		except FileNotFoundError:
			pass #Test just didn't write to the file

	def test_new_title(self):
		new_title = "This is a new title"
		self.writer.title = new_title
		self.assertTrue(new_title in str(self.writer), "Title was not updated")
		self.assertTrue(self.validator.validate(), self.validator.failures)

	def test_paragraph(self):
		text = "This is a paragraph"
		self.writer.text(text)
		self.assertTrue(self.validator.validate(), self.validator.failures)
		self.assertTrue(text in self.writer.to_text(), "Paragraph was not included")

	def test_admonition(self):
		admonition_type = "DANGER"
		text = "Beware of the killer rabbits"
		d = self.writer.directive(admonition_type)
		d.text(text)
		self.assertTrue(self.validator.validate(), self.validator.failures)

	def test_image(self):
		file = "image.png"
		img = self.writer.directive("image", file)
		img.option("width", 500)
		img.option("height", 100)
		self.assertTrue(self.validator.validate(), self.validator.failures)

	def test_doctest(self):
		test_line = 'print("test")'
		expected_output = 'test'
		self.writer.doctest(test_line, expected_output)
		self.assertTrue(test_line in self.writer.to_text(), "DocTest test line was not included")
		self.assertTrue(expected_output in self.writer.to_text(), "DocTest expected output was not included")
		self.assertTrue(self.validator.validate(), self.validator.failures)

	def test_lists(self):
		items = ["Test 1", 2, 16.4, True]
		self.writer.bulleted_list(*items)
		self.assertTrue(self.validator.validate(), self.validator.failures)
		self.writer.clear()
		self.writer.enumerated_list(*items)
		self.assertTrue(self.validator.validate(), self.validator.failures)

	def test_field(self):
		name = "TestField"
		text = "This is a field"
		self.writer.field(name, text)
		self.assertTrue(self.validator.validate(), self.validator.failures)
		self.assertTrue(name in self.writer.to_text(), "Field name was not included")
		self.assertTrue(text in self.writer.to_text(), "Field text was not included")


	def test_table(self):
		tab = [
			[0, 1, 2, 3],
			[4, 5, 6, 7],
			[8, 9, 10, 11]
		]
		headings = ["Column 1", "Column 2", "Column 3", "Column 4"]
		self.writer.simple_table(tab, column_headings=headings)
		self.assertTrue(self.validator.validate(), self.validator.failures)



	def test_section(self):
		text = "This is inside a section"
		sect = self.writer.section("Section")
		sect.text(text)
		self.assertTrue(text in str(self.writer), f"Subsection text was not included")
		self.assertTrue(self.validator.validate(), self.validator.failures)

	def test_write(self):
		self.writer.write_to_file(self.file)
		with open(self.file, "w") as f:
			self.writer.write_to_file(f)

		with self.assertRaises(ValueError):
			self.writer.write_to_file("")

		with self.assertRaises(ValueError):
			self.writer.write_to_file(None)

		with self.assertRaises(TypeError):
			self.writer.write_to_file(12)


if __name__ == '__main__':
	unittest.main()
