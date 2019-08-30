import unittest
import os


def main():
    loader = unittest.TestLoader()
    cwd = os.getcwd()
    suite = loader.discover(cwd)
    runner = unittest.TextTestRunner()
    runner.run(suite)


if __name__ == '__main__':
    main()
