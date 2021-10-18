import os
import sys

# The current working directory
cwd = os.path.dirname(__file__)

# The top-level testing directory
tests_dir = os.path.join(cwd, "..")

# The root directory of the project
root_dir  = os.path.join(tests_dir, "..")
sys.path.insert(0, os.path.abspath(root_dir))

import cminx

# Here we work out some paths for the convenience of the test suite

# The directory containing examples
example_dir = os.path.abspath(os.path.join(tests_dir, "examples"))

# The examples.cmake file in the example_dir
example_cmake = os.path.join(example_dir, "example.cmake")

# The directory
