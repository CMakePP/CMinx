# cminx
[![Build Status](https://travis-ci.com/CMakePP/CMakeDoc.svg?branch=master)](
https://travis-ci.com/CMakePP/CMakeDoc)
[![codecov](
https://codecov.io/gh/CMakePP/CMakeDoc/branch/master/graph/badge.svg)](
https://codecov.io/gh/CMakePP/CMakeDoc)
[![Documentation Status](https://readthedocs.org/projects/cmakedoc/badge/?version=latest)](https://cmakedoc.readthedocs.io/en/latest/?badge=latest)

A common software practice is to keep documentation close to the functions and
classes that are being documented (ideally in the same source file). Most
languages have mechanisms for doing this for example Python has docstrings and
C++ has Doxygen. To our knowledge no such solution exists for CMake. CMinx
fixes this.

CMinx is a Python package that extracts documentation from CMake source
files. CMake developers document their functions by immediately proceeding the
function with a comment block written in reStructuredText (reST). CMinx will
extract the comment blocks verbatim and create `*.rst` files which can be
included in a normal Sphinx documentation set-up.

## Installing
You can find installation instructions here: [How to install](docs/source/installation.rst)


## Usage
For each CMake function or variable that you would like to document, prepend it with a block doc-comment.
A block doc-comment begins with `#[[[` and ends with `#]]`.

Then run `cminx` on your CMake files, outputting to a directory of your choosing. The help text is printed below for reference:
```
Usage: cminx [-h] [-o OUTPUT] [-r] file [file ...]

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
Here we show an example CMake file, called `example.cmake`, that contains
doccomments documenting functions, macros, and variables.
The file contents are shown below.

example.cmake:
```cmake                                                                                      
#[[
# This is a normal block comment and
# will not be treated as a doccomment.
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
# This is an example of variable documentation.
# This variable is a list of string values.
#]]
set(MyList "Value" "Value 2")


#[[[
# This is another example of variable documentation.
# This variable is a string variable.
#]]
set(MyString "String")

```

To generate the documentation, we enter our system shell (example assumes Bash-like shell on a Unix-like system).

Generating documentation in directory `output`:
```console
foo@bar:~$ cminx -o output/ example.cmake
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

   
   This macro says hi.
   This documentation uses a differing format,
   but is still processed correctly.
   
   :param person: The person we want to greet.
   :type person: string 
   


.. data:: MyList
   
   This is an example of variable documentation.
   This variable is a list of string values.
   

   :Default value: ['"Value"', '"Value 2"']

   :type: VarType.List


.. data:: MyString
   
   This is another example of variable documentation.
   This variable is a string variable.
   

   :Default value: String

   :type: VarType.String



```
