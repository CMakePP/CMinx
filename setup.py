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

# Get the version from the git tag
git_cmd = ['git', 'describe', '--tags', '--abbrev=0']
version = subprocess.check_output(git_cmd).strip().decode()[1:]

# This will fail if requirements.txt not found, as it should
with open("requirements.txt", "r") as f:
    dependencies = f.read().split()

setup(
    name='CMinx',
    version=version,
    description='Documentation Generator for the CMake language',
    author='CMakePP',
    author_email='bwtbutler@hotmail.com',
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
    install_requires=dependencies
)
