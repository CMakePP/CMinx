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
import context
import unittest
import os
import shutil
import sys
import context
import cminx
import helpers

class TestInit(unittest.TestCase):
    """ Tests the functions found in __init__.py
    """

    def setUp(self):
        self.cwd = os.path.abspath(os.path.dirname(__file__))
        self.input_dir = context.example_dir
        self.output_dir = os.path.join(self.cwd, "output")
        self.input_file = context.example_cmake
        self.output_file = os.path.join(self.output_dir, "example.rst")

    def tearDown(self):
        try:
            shutil.rmtree(self.output_dir)
            pass
        except FileNotFoundError:
            pass #Test just didn't write to the directory


    def test_document(self):
      """Tests the document command in the CMinx module"""
      sys.stdout = open(os.devnull, 'w')
      cminx.document(self.input_file, self.output_dir, True)
      sys.stdout = sys.__stdout__

      # Test that the top-level directory was found
      is_dir = os.path.isdir(self.output_dir)
      self.assertTrue(is_dir, "Output directory structure incorrect")

      # Test that the file is in the directory
      is_file = os.path.isfile(self.output_file)
      self.assertTrue(is_file, "Output file does not exist")


    def test_document_prefix(self):
      """Tests the document command in the CMinx module with the prefix option"""
      sys.stdout = open(os.devnull, 'w')
      cminx.document(self.input_file, self.output_dir, recursive=True, prefix=context.prefix)
      sys.stdout = sys.__stdout__

      # Test that the top-level directory was found
      is_dir = os.path.isdir(self.output_dir)
      self.assertTrue(is_dir, "Output directory structure incorrect")

      # Test that the file is in the directory
      is_file = os.path.isfile(self.output_file)
      self.assertTrue(is_file, "Output file does not exist")

    def test_recursive(self):
      """Tests the use of CMinx in recursive mode"""
      args = ["-r", "-o", self.output_dir, self.input_dir]
      helpers.quiet_cminx(args)

      # Test that the top-level directory was found
      is_dir = os.path.isdir(self.output_dir)
      self.assertTrue(is_dir, "Output directory structure incorrect")

      # Test that reST file is in top-level directory
      is_file = os.path.isfile(self.output_file)
      self.assertTrue(is_file, "Output file does not exist")

      diff = helpers.diff_files(self.output_file, context.corr_example_rst)
      self.assertTrue(diff == "")

    def test_recursive_prefix(self):
      """Tests the use of CMinx in recursive mode with a prefix"""
      args = ["-r", "-p", context.prefix, "-o", self.output_dir, self.input_dir]
      helpers.quiet_cminx(args)

      # Test that the top-level directory was found
      is_dir = os.path.isdir(self.output_dir)
      self.assertTrue(is_dir, "Output directory structure incorrect")

      # Test that reST file is in top-level directory
      is_file = os.path.isfile(self.output_file)
      self.assertTrue(is_file, "Output file does not exist")

      diff = helpers.diff_files(self.output_file, context.corr_example_prefix_rst)

      self.assertTrue(diff == "")

if __name__ == '__main__':
    unittest.main()
