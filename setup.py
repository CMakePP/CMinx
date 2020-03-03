#!/usr/bin/env python3

import os

from setuptools import setup

#Split the prefix and var so they aren't automatically replaced by CMake
prefix = "$"
var = '{CMAKE_CURRENT_SOURCE_DIR}'
dir = '${CMAKE_CURRENT_SOURCE_DIR}' #This will be replaced by CMake and will therefore not equal prefix+var

version = None
with open("version.txt", "r") as f:
      version = f.read().strip()

config = {
      'name': 'CMakeDoc',
      'version': version,
      'description': 'Documentation Generator for the CMake language',
      'author': 'Branden Butler',
      'author_email': 'bwtbutler@hotmail.com',
      'url': 'https://github.com/CMakePP/CMakeDoc',
      'packages': ['cmakedoc', 'cmakedoc.parser'],
      'entry_points': {
        'console_scripts': [
            'cmakedoc = cmakedoc:main'
        ]
      },
      'package_data':  {
           "": ["*.g4", "*.interp", "*.tokens"]
      },
      'install_requires':  [
          "antlr4-python3-runtime",
      ]
     }

#Check to see if running under CMake
if not ((prefix + var) == dir):
	config.update({'package_dir': { 'cmakedoc':  os.path.join(dir, "cmakedoc")}})


setup(**config)
