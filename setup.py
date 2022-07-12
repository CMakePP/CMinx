#!/usr/bin/env python3
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
import subprocess
from setuptools import setup

# Get the absolute path to the directory
script_path = os.path.realpath(__file__)
script_dir = os.path.dirname(script_path)

# Get the version from the git tag
git_cmd = ['git', 'describe', '--tags', '--abbrev=0']
#git_out = subprocess.check_output(git_cmd, cwd=script_dir)
cminx_version = 0.1 # git_out.strip().decode()[1:]

# This will fail if requirements.txt not found, as it should
requirements_path = os.path.join(script_dir, "requirements.txt")
with open(requirements_path, "r") as f:
    dependencies = f.read().split()

# Get the long description from the README
readme_path = os.path.join(script_dir, "README.md")
with open(readme_path, "r") as f:
    long_desc = f.read()

setup(
    name='CMinx',
    version=cminx_version,
    description='Documentation Generator for the CMake language',
    long_description=long_desc,
    long_description_content_type="text/markdown",
    author='CMakePP',
    author_email='cmakepp@gmail.com',
    url='https =//github.com/CMakePP/CMinx',
    packages=['cminx', 'cminx.parser'],
    entry_points={
        'console_scripts': [
            'cminx = cminx:main',
        ],
    },
    package_data={
        "": ["*.g4", "*.interp", "*.tokens", "*.yaml"]
    },
    install_requires=dependencies,
    classifiers=[
        "Programming Language :: Python :: 3"
    ]
)
