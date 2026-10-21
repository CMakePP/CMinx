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
import unittest

import context
import helpers


class TestConfig(unittest.TestCase):
    """
    Tests the functionality of the configuration system
    """

    def setUp(self):
        self.cwd = os.path.abspath(os.path.dirname(__file__))
        self.input_dir = context.example_dir
        self.output_dir = os.path.join(self.cwd, "output")
        self.input_file = context.example_cmake
        self.output_file = os.path.join(self.output_dir, "example.rst")
        self.output_index_file = os.path.join(self.output_dir, "index.rst")
        self.config_dir = context.config_dir
        self.maxDiff = None

    def tearDown(self):
        try:
            shutil.rmtree(self.output_dir)
            pass
        except FileNotFoundError:
            pass  # Test just didn't write to the directory

    def test_no_undocumented(self):
        """Tests include_undocumented_* settings as False"""
        args = ["-r", "-o", self.output_dir, "-s", context.no_include_undocumented_config, self.input_dir]
        helpers.quiet_cminx(args)

        # Test that the top-level directory was found
        is_dir = os.path.isdir(self.output_dir)
        self.assertTrue(is_dir, "Output directory structure incorrect")

        # Test that reST file is in top-level directory
        is_file = os.path.isfile(self.output_file)
        self.assertTrue(is_file, "Output file does not exist")

        with open(context.corr_example_no_undocumented, 'r') as corr_file, open(self.output_file, 'r') as generated_file:
            self.assertEqual(corr_file.read(), generated_file.read())

        with open(context.corr_index_rst, 'r') as corr_file, open(self.output_index_file, 'r') as generated_file:
            self.assertEqual(corr_file.read(), generated_file.read())

    def test_no_auto_exclude(self):
        """Tests auto_exclude_directories_as_cmake setting as False"""
        args = ["-r", "-o", self.output_dir, "-s", context.no_auto_exclude_config, self.input_dir]
        helpers.quiet_cminx(args)

        # Test that the top-level directory was found
        is_dir = os.path.isdir(self.output_dir)
        self.assertTrue(is_dir, "Output directory structure incorrect")

        # Test that reST file is in top-level directory
        is_file = os.path.isfile(self.output_file)
        self.assertTrue(is_file, "Output file does not exist")

        with open(context.corr_example_rst, 'r') as corr_file, open(self.output_file, 'r') as generated_file:
            self.assertEqual(corr_file.read(), generated_file.read())

        with open(context.corr_index_no_auto_exclude, 'r') as corr_file, open(self.output_index_file, 'r') as generated_file:
            self.assertEqual(corr_file.read(), generated_file.read())

    def test_exclude_filters(self):
        """Tests the gitignore-like exclusion filters"""
        args = ["-r", "-o", self.output_dir, "-s", context.exclusion_filters_config, self.input_dir]
        helpers.quiet_cminx(args)

        # Test that the top-level directory was found
        is_dir = os.path.isdir(self.output_dir)
        self.assertTrue(is_dir, "Output directory structure incorrect")

        # Test that reST file is in top-level directory
        is_file = os.path.isfile(self.output_file)
        self.assertTrue(is_file, "Output file does not exist")

        with open(context.corr_example_rst, 'r') as corr_file, open(self.output_file, 'r') as generated_file:
            self.assertEqual(corr_file.read(), generated_file.read())

        with open(context.corr_index_exclusion_filters, 'r') as corr_file, open(self.output_index_file,
                                                                              'r') as generated_file:
            self.assertEqual(corr_file.read(), generated_file.read())

    def test_exclude_input(self):
        """Tests the gitignore-like exclusion filters"""
        args = ["-o", self.output_dir, "-s", context.exclude_input_file_config, self.input_file]
        helpers.quiet_cminx(args)

        # Test that the top-level directory was not found, since we don't do anything
        is_dir = os.path.exists(self.output_dir)
        self.assertFalse(is_dir, "Output directory structure created when input should've been ignored")

    def test_exclude_filters_adjacent(self):
        """Tests that exclusion filters apply to adjacent files and directories"""
        input_dir = os.path.join(self.cwd, "adjacent_input")
        self.addCleanup(shutil.rmtree, input_dir, ignore_errors=True)
        # Exclude all but one entry, so that whatever order os.walk() returns
        # them in, some excluded entries are adjacent
        for name in ["a", "b", "c", "d", "keep"]:
            os.makedirs(os.path.join(input_dir, name + "_dir"))
            for path in [os.path.join(input_dir, name + ".cmake"),
                         os.path.join(input_dir, name + "_dir", "file.cmake")]:
                with open(path, 'w') as f:
                    f.write("function(func)\nendfunction()\n")

        exclude_args = []
        for name in ["a", "b", "c", "d"]:
            exclude_args.extend(["-e", name + ".cmake", "-e", name + "_dir/"])
        args = ["-r", "-o", self.output_dir] + exclude_args + [input_dir]
        helpers.quiet_cminx(args)

        generated = sorted(
            os.path.relpath(os.path.join(root, file), self.output_dir)
            for root, _, files in os.walk(self.output_dir) for file in files)
        self.assertEqual(
            ["index.rst", "keep.rst",
             os.path.join("keep_dir", "file.rst"), os.path.join("keep_dir", "index.rst")],
            generated)



if __name__ == '__main__':
    unittest.main()
