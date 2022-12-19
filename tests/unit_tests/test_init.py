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
import os
import shutil
import sys
import unittest

import context
import helpers

import cminx
from cminx.config import Settings, InputSettings, OutputSettings, RSTSettings, LoggingSettings


class TestInit(unittest.TestCase):
    """
    Tests the functions found in __init__.py
    """

    def setUp(self):
        self.cwd = os.path.abspath(os.path.dirname(__file__))
        self.input_dir = context.example_dir
        self.output_dir = os.path.join(self.cwd, "output")
        self.input_file = context.example_cmake
        self.output_file = os.path.join(self.output_dir, "example.rst")
        self.output_index_file = os.path.join(self.output_dir, "index.rst")
        self.maxDiff = None

    def tearDown(self):
        try:
            shutil.rmtree(self.output_dir)
            pass
        except FileNotFoundError:
            pass  # Test just didn't write to the directory

    def test_document(self):
        """Tests the document command in the CMinx module"""
        sys.stdout = open(os.devnull, 'w')
        cminx.document(self.input_file,
                       Settings(InputSettings(recursive=True), OutputSettings(directory=self.output_dir)))
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
        cminx.document(self.input_file,
                       Settings(input=InputSettings(recursive=True), output=OutputSettings(directory=self.output_dir),
                                rst=RSTSettings(prefix=context.prefix)))
        sys.stdout = sys.__stdout__

        # Test that the top-level directory was found
        is_dir = os.path.isdir(self.output_dir)
        self.assertTrue(is_dir, "Output directory structure incorrect")

        # Test that the file is in the directory
        is_file = os.path.isfile(self.output_file)
        self.assertTrue(is_file, "Output file does not exist")

    def test_header_extensions_no_undocumented_diff_header(self):
        input_settings = InputSettings(include_undocumented_ct_add_test=False, include_undocumented_cpp_attr=False,
                                       include_undocumented_function=False, include_undocumented_cpp_class=False,
                                       include_undocumented_macro=False, include_undocumented_cpp_member=False,
                                       include_undocumented_ct_add_section=False, include_undocumented_add_test=False,
                                       recursive=True)
        output_settings = OutputSettings(directory=self.output_dir)
        rst_settings = RSTSettings(file_extensions_in_modules=True, file_extensions_in_titles=True,
                                   headers=['^', '*', '=', '-', '_', '~', '!', '&', '@'])
        settings = Settings(input_settings, output_settings, LoggingSettings(), rst_settings)
        cminx.document(self.input_dir, settings)
        # diff = helpers.diff_files(self.output_file, context.corr_example_no_undocumented_diff_header)
        # self.assertEqual(diff, "")
        with open(context.corr_example_no_undocumented_diff_header, 'r') as corr_file, \
                open(self.output_file, 'r') as generated_file:
            self.assertEqual(corr_file.read(), generated_file.read())

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

        with open(context.corr_example_rst, 'r') as corr_file, open(self.output_file, 'r') as generated_file:
            self.assertEqual(corr_file.read(), generated_file.read())

        with open(context.corr_index_rst, 'r') as corr_file, open(self.output_index_file, 'r') as generated_file:
            self.assertEqual(corr_file.read(), generated_file.read())

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

        with open(context.corr_example_prefix_rst, 'r') as corr_file, open(self.output_file, 'r') as generated_file:
            self.assertEqual(corr_file.read(), generated_file.read())

        with open(context.corr_index_prefix_rst, 'r') as corr_file, open(self.output_index_file, 'r') as generated_file:
            self.assertEqual(corr_file.read(), generated_file.read())

    def test_nonexistent_input(self):
        """Tests whether trying to document a nonexistent file exits with -1"""
        args = ["nonexistent-file.cmake"]
        exit_code = None
        try:
            helpers.quiet_cminx(args)
        except SystemExit as e:
            exit_code = e.code

        self.assertEqual(-1, exit_code, f"Exit code for nonexistent input incorrect (None means did not exit):"
                                        "{exit_code}")


if __name__ == '__main__':
    unittest.main()
