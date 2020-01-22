#!/usr/bin/env python3

from setuptools import setup

setup(name='CMakeDoc',
      version='1.0',
      description='Documentation Generator for the CMake language',
      author='Branden Butler',
      author_email='bwtbutler@hotmail.com',
      url='https://github.com/CMakePP/CMakeDoc',
      packages=['cmakedoc', 'cmakedoc.parser'],
      entry_points={
        'console_scripts': [
            'cmakedoc = cmakedoc:main'
        ]
      },
      package_data = {
           "": ["*.g4", "*.interp", "*.tokens"]
      },
      install_requires = [
          "antlr4-python3-runtime",
      ]
     )
