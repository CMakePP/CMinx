#!/usr/bin/python3
import context
import unittest
import os
import shutil

class TestSamples(unittest.TestCase):

    def setUp(self):
        self.cwd = os.path.abspath(os.path.dirname(__file__))
        self.output_dir = os.path.join(self.cwd, "output")


    def tearDown(self):
        try:
            shutil.rmtree(self.output_dir)
            pass
        except FileNotFoundError:
            pass


    def test_samples(self):
        for f in os.listdir(self.cwd):
            prefix = f.split(".cmake")[0]
            print(prefix)
