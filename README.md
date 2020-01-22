# CMakeDoc
[![Build Status](https://travis-ci.com/CMakePP/CMakeDoc.svg?branch=master)](
https://travis-ci.com/CMakePP/CMakeDoc)
[![codecov](
https://codecov.io/gh/CMakePP/CMakeDoc/branch/master/graph/badge.svg)](
https://codecov.io/gh/CMakePP/CMakeDoc)
[![Documentation Status](
https://readthedocs.org/projects/cmakedoc/badge/?version=latest)](
https://cmakedoc.readthedocs.io/en/latest/?badge=latest)

A common software practice is to keep documentation close to the functions and
classes that are being documented (ideally in the same source file). Most
languages have mechanisms for doing this for example Python has docstrings and
C++ has Doxygen. To our knowledge no such solution exists for CMake. CMakeDoc
fixes this.

CMakeDoc is a Python package that extracts documentation from CMake source
files. CMake developers document their functions by immediately proceeding the
function with a comment block written in reStructuredText (reST). CMakeDoc will
extract the comment blocks verbatim and create `*.rst` files which can be
included in a normal Sphinx documentation set-up.

## Installing

#### With PIP / PyPI
Run:
```console
foo@bar:~$ sudo pip3 install cmakedoc
```

#### Manually
Run the following commands one at a time:

```console
foo@bar:~$ git clone github.com/CMakePP/CMakeDoc.git
foo@bar:~$ cd CMakeDoc/
foo@bar:~/CMakeDoc$ sudo pip3 install . #If pip installed
foo@bar:~/CMakeDoc$ sudo python3 setup.py install #If pip not installed
```

## Usage
For each CMake function or variable that you would like to document, prepend it with a block doc-comment.
A block doc-comment begins with `#[[[` and ends with `#]]`.

Then run `cmakedoc` on your CMake files, outputting to a directory of your choosing. The help text is printed below for reference:
```
Usage: cmakedoc [-h] [-o OUTPUT] [-r] file [file ...]

positional arguments:
  file                  CMake file to generate documentation for. If
                        directory, will generate documentation for all *.cmake
                        files (case-insensitive)

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Directory to output generated RST to. If not specified
                        will print to standard output. Output files will have
                        the original filename with the cmake extension
                        replaced by .rst
  -r, --recursive       If specified, will generate documentation for all
                        subdirectories of specified directory recursively
```

### Example
example.cmake:
```cmake                                                                                      
#[[
# THIS SHOULD BE SKIPPED
#]]
include_guard()

#[[[
# This function has very basic documentation.
#
# This function's description stays close to idealized formatting and does not do
# anything fancy.
#
# :param person: The person this function says hi to
# :param me: What my name is
# :type person: string
# :type me: string
#]]
function(say_hi_to person me)
    message("Hi ${person}, I am ${me}")
endfunction()

#[[[
# This macro says hi
#]]
macro(macro_say_hi person)
   message("Hi ${person}")
endmacro()


#[[[
# list
#]]
set(MyList "Value" "Value 2")


#[[[
# string
#]]
set(MyString "String")

```

Generating documentation in directory `output`:
```console
foo@bar:~$ cmakedoc -o output/ example.cmake
Writing RST files to /home/foo/output
Writing for file /home/foo/example.cmake
Writing RST file /home/foo/output/example.rst
foo@bar:~$ cat output/example.rst
#######################
/home/foo/example.cmake
#######################

.. function:: say_hi_to(person me)
   
   This function has very basic documentation.
   
   This function's description stays close to idealized formatting and does not do
   anything fancy.
   
   :param person: The person this function says hi to
   :param me: What my name is
   :type person: string
   :type me: string
   


.. function:: macro_say_hi(person)

   .. warning:: This is a macro, and so does not introduce a new scope.

   
   This macro says hi
   


.. data:: MyList
   
   list
   

   :Default value: ['"Value"', '"Value 2"']

   :type: VarType.List


.. data:: MyString
   
   string
   

   :Default value: String

   :type: VarType.String



```
