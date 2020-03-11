#!/usr/bin/python3
import context
import unittest
import sys
import os
import shutil
import cminx


class TestInit(unittest.TestCase):

    def setUp(self):
        self.input_file_prefix = "example"
        self.input_file_postfix = "cmake"
        self.input_dir = "test_samples"
        self.input_path = os.path.join(self.input_dir, self.input_file_prefix + "." + self.input_file_postfix)
        self.output_dir = os.path.join(os.getcwd(), "output")
        self.output_file_postfix = "rst"

    def tearDown(self):
                try:
                        shutil.rmtree(self.output_dir)
                        #pass
                except FileNotFoundError:
                        pass #Test just didn't write to the directory


    def test_document(self):
      cminx.document(self.input_path, self.output_dir, True)
      self.assertTrue(os.path.isfile(os.path.join(self.output_dir, self.input_file_prefix + "." + self.output_file_postfix)), "Output file does not exist")

    def test_recursive(self):
      args = ["-r", "-o", self.output_dir, os.getcwd()]
      cminx.main(args)
      self.assertTrue(os.path.isdir(os.path.join(self.output_dir, self.input_dir)), "Output directory structure incorrect")
      self.assertTrue(os.path.isfile(os.path.join(os.path.join(self.output_dir, self.input_dir), self.input_file_prefix + "." + self.output_file_postfix)), "Output file does not exist")


if __name__ == '__main__':
    unittest.main()
