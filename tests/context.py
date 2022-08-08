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
root_dir = os.path.join(tests_dir, "..")
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

# The directory containing test_samples
test_samples_dir = os.path.abspath(os.path.join(tests_dir, "test_samples"))

# The correct examples.rst file
corr_example_rst = os.path.join(example_sphinx, "source", "example.rst")

# The correct index.rst file
corr_index_rst = os.path.join(test_samples_dir, "corr_rst", "index", "index.rst")

# The correct examples.rst file, with context.prefix as a prefix
corr_example_prefix_rst = os.path.join(example_sphinx, "source", "example_prefix.rst")

# The correct index.rst file, with context.prefix as a prefix
corr_index_prefix_rst = os.path.join(test_samples_dir, "corr_rst", "index", "index_prefix.rst")

corr_example_no_undocumented_diff_header = os.path.join(example_sphinx, "source",
                                                        "example_no_undocumented_diff_header.rst")

corr_example_no_undocumented = os.path.join(example_sphinx, "source", "example_no_undocumented.rst")

corr_index_no_auto_exclude = os.path.join(example_sphinx, "source", "index_no_auto_exclude.rst")

corr_index_exclusion_filters = os.path.join(example_sphinx, "source", "index_exclusion_filters.rst")

# Where the example configs are located
config_dir = os.path.join(example_dir, "configs")

# The config that sets all the input.include_undocumented_* settings to False
no_include_undocumented_config = os.path.join(config_dir, "no_include_undocumented_config.yaml")

# The config that sets auto_exclude_directories_without_cmake to False
no_auto_exclude_config = os.path.join(config_dir, "no_auto_exclude_config.yaml")

# The config that sets the exclusion filters to ignore more_cmake_files/
exclusion_filters_config = os.path.join(config_dir, "exclude_filters_config.yaml")

# The config that excludes example.cmake
exclude_input_file_config = os.path.join(config_dir, "exclude_input_file_config.yaml")
