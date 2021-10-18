#!/usr/bin/python3
import context
import unittest
import sys
import os
import shutil
import context
import cminx


class TestInit(unittest.TestCase):
    """ Tests the functions found in __init__.py
    """

    def setUp(self):
        self.cwd = os.path.abspath(os.path.dirname(__file__))
        self.input_file_prefix = "example"
        self.input_file_postfix = "cmake"
        self.input_dir = context.example_dir
        self.input_path = os.path.join(context.example_cmake)
        self.output_dir = os.path.join(self.cwd, "output")
        self.output_file_postfix = "rst"

    def tearDown(self):
        print("calling tearDown")
        try:
            shutil.rmtree(self.output_dir)
            pass
        except FileNotFoundError:
            pass #Test just didn't write to the directory


    def test_document(self):
      print("running test_document")
      cminx.document(self.input_path, self.output_dir, True)
      self.assertTrue(os.path.isfile(os.path.join(self.output_dir, self.input_file_prefix + "." + self.output_file_postfix)), "Output file does not exist")

    def test_recursive(self):
      print("running test_recursive")
      args = ["-r", "-o", self.output_dir, self.cwd]
      cminx.main(args)
      out_file_name = self.input_file_prefix + "." + self.output_file_postfix
      top_dir = os.path.join(self.output_dir, self.input_dir)
      file_path = os.path.join(self.output_dir, out_file_name)
      print(file_path)
      self.assertTrue(os.path.isdir(top_dir), "Output directory structure incorrect")
      self.assertTrue(os.path.isfile(file_path), "Output file does not exist")


if __name__ == '__main__':
    unittest.main()
