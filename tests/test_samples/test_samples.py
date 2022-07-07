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
import helpers


class TestSamples(unittest.TestCase):

    def setUp(self):
        self.cwd = os.path.abspath(os.path.dirname(__file__))
        self.output_dir = os.path.join(self.cwd, "output")
        self.input_dir = context.test_samples_dir

        # Directory containing the correct answers
        self.corr_dir = os.path.join(self.cwd, "corr_rst")

    def tearDown(self):
        try:
            shutil.rmtree(self.output_dir)
            pass
        except FileNotFoundError:
            pass

    def test_samples(self):
        args = ["-r", "-o", self.output_dir, self.input_dir]
        helpers.quiet_cminx(args)
        for f in os.listdir(self.cwd):
            if ".cmake" not in f:
                continue
            prefix = f.split(".cmake")[0]
            file_name = prefix + ".rst"
            generated_path = os.path.join(self.output_dir, file_name)
            corr_path = os.path.join(self.corr_dir, file_name)
            with open(corr_path, 'r') as corr_file, open(generated_path, 'r') as generated_file:
                self.assertEqual(corr_file.read(), generated_file.read())
