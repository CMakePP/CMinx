#!/usr/bin/python3
import context
import unittest
import os
import shutil
import helpers


class TestSamples(unittest.TestCase):

    def setUp(self):
        self.cwd = os.path.abspath(os.path.dirname(__file__))
        self.output_dir = os.path.join(self.cwd, "output")
        self.input_dir  = context.test_samples_dir

        # Directory containing the correct answers
        self.corr_dir   = os.path.join(self.cwd, "corr_rst")

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
            if not ".cmake" in f:
                continue
            prefix = f.split(".cmake")[0]
            file_name = prefix + ".rst"
            generated_path = os.path.join(self.output_dir, file_name)
            corr_path = os.path.join(self.corr_dir, file_name)
            diff = helpers.diff_files(generated_path, corr_path)
            self.assertTrue(diff == "")
