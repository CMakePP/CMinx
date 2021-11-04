.. Copyright 2021 CMakePP
..
.. Licensed under the Apache License, Version 2.0 (the "License");
.. you may not use this file except in compliance with the License.
.. You may obtain a copy of the License at
..
.. http://www.apache.org/licenses/LICENSE-2.0
..
.. Unless required by applicable law or agreed to in writing, software
.. distributed under the License is distributed on an "AS IS" BASIS,
.. WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
.. See the License for the specific language governing permissions and
.. limitations under the License.
..
#####
Usage
#####

For each CMake function or variable that you would like to document, prepend it 
with a block doc-comment. A block doc-comment begins with :code:`#[[[` and ends 
with :code:`#]]`.

Then run :code:`cminx` on your CMake files, outputting to a directory of your 
choosing. The help text is printed below for reference::

   Usage: cminx [-h] [-o OUTPUT] [-r] file [file ...]

   positional arguments:
      file                 CMake file to generate documentation for. If 
                           directory, will generate documentation for all 
                           *.cmake files (case-insensitive)

   optional arguments:
     -h, --help            show this help message and exit
     -o OUTPUT, --output OUTPUT
                           Directory to output generated RST to. If not 
                           specified will print to standard output. Output files 
                           will have the original filename with the cmake 
                           extension replaced by .rst
     -r, --recursive       If specified, will generate documentation for all
                           subdirectories of specified directory recursively