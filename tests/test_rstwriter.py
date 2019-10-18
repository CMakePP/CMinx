#!/usr/bin/python3

from cmakedoc.rstwriter import RSTWriter
import unittest
import os

class TestRSTWriter(unittest.TestCase):
	def setUp(self):
		self.writer = RSTWriter("Testing RSTWriter")
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

	def test_lists(self):
		items = ["Test 1", 2, 16.4, True]
		self.writer.bulleted_list(*items)
		for item in items:
			self.assertTrue(str(item) in str(self.writer), f"Bulleted list not complete, missing {item}")
		self.writer.clear()
		self.writer.enumerated_list(*items)
		for item in items:
                        self.assertTrue(str(item) in str(self.writer), f"Enumerated list not complete, missing {item}")

	def test_field(self):
		name = "TestField"
		text = "This is a field"
		self.writer.field(name, text)
		self.assertTrue(f":{name}: {text}" in str(self.writer))

	def test_section(self):
		text = "This is inside a section"
		sect = self.writer.section("Section")
		sect.text(text)
		self.assertTrue(text in str(self.writer), f"Writer is {self.writer}") #Makes sure subsection is included in root

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
