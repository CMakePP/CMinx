#!/usr/bin/python3

import unittest
import os



def main():
    loader = unittest.TestLoader()
    cwd = os.path.abspath(os.path.dirname(__file__))

    suite_names = ["test_samples", "unit_tests"]
    suite_paths = [os.path.join(cwd, x) for x in suite_names]
    suites = loader.discover(cwd, "test_*.py")
    all_tests = unittest.TestSuite(suites)
    runner = unittest.TextTestRunner()
    runner.run(all_tests)


if __name__ == '__main__':
    main()
