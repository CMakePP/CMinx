################################################################################
#
# file: context.py
#
# This file contains paths and other helpful information used throughout the
# test suites of CMinx
#
################################################################################

import os
import sys

# The current working directory
tests_dir = os.path.dirname(__file__)

# The root directory of the project
root_dir  = os.path.join(tests_dir, "..")
sys.path.insert(0, os.path.abspath(root_dir))

import cminx

# Here we work out some paths for use throughout the test suite

# The directory containing examples
example_dir = os.path.abspath(os.path.join(tests_dir, "examples"))

# The examples.cmake file in the example_dir
example_cmake = os.path.join(example_dir, "example.cmake")

# The sphinx directory in the example_dir
example_sphinx = os.path.join(example_dir, "sphinx")

# A prefix to be used to test CMinx's prefix option.
prefix = "prefix"

# The correct examples.rst file
corr_example_rst = os.path.join(example_sphinx, "source", "example.rst")

# The correct examples.rst file, with context.prefix as a prefix
corr_example_prefix_rst = os.path.join(example_sphinx, "source", "example_prefix.rst")

# The directory containing test_samples
test_samples_dir = os.path.abspath(os.path.join(tests_dir, "test_samples"))
