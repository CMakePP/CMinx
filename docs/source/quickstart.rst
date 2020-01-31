----------
Quickstart
----------

.. note::

   This tutorial assumes you are familiar with reStructuredText (reST) and
   CMake.

According to CMakeDoc, the contents of a CMake file can be broken into three
categories:

#. Documentation comments - what CMakeDoc extracts

#. Annotation comments - Comments that are not documentation

#. CMake source code - Everything else

To distinguish between the two types of comments CMakeDoc borrows the convention
that documentation comments start with an additional comment character. Thus to
indicate that a CMake comment is documentation use :code:`#[[[` (the block
comment should still end with :code:`#]]`).

The contents of the documentation comments should follow usual Python reST
conventions. In other words:

.. code:: cmake

   #[[[ 
   # Short description. Runs up to the first blank line. So this is still the
   # short description.
   #
   # Longer description goes here and includes all text and paragraphs from
   # here forward that are not part of reST directives.
   #
   # The parameters, keywords, and their types will be pulled out of the longer
   # description and placed in separate sections regardless of where they
   # appear.
   #
   # :param name_of_param: Description of what `name_of_param` is used for
   #
   # The next line is a reST directive and will not be part of the longer
   # description.
   #
   # .. note::
   #
   #    This is a note, it will show up using reST's native note section
   #]]

Technically speaking the contents of the comments are dumped more-or-less
verbatim into the resulting ``*.rst`` file so you can use any reST directives
and markup you like. That said, you will probably only want to use:

- ``:param <name of parameter>: <description of parameter>``
- ``:type <name of parameter>: <type of parameter named "name of parameter">``
- ``:keyword <name of keyword>: <description of keyword>``

as those are the subset of Python language features CMake actually supports.

##########
Installing
##########

======================================
With PIP / PyPI in Virtual Environment
======================================

Run:

.. code:: console

   foo@bar:~$ mkdir virt-env #Directory for our virtual environment
   foo@bar:~$ python3 -m venv virt-env && cd virt-env #Create our virtual environment and enter the directory
   foo@bar:~/virt-env$ source ./bin/activate #Activate virtual environment
   (virt-env) foo@bar:~/virt-env$ pip3 install cmakedoc #Install package in virt-env

========
Manually
========

Run the following commands one at a time:

.. code:: console

   foo@bar:~$ git clone github.com/CMakePP/CMakeDoc.git
   foo@bar:~$ cd CMakeDoc/
   foo@bar:~/CMakeDoc$ mkdir virt-env #Directory for our virtual environment
   foo@bar:~/CMakeDoc$ python3 -m venv virt-env && cd virt-env #Create our virtual environment and enter the directory
   foo@bar:~/CMakeDoc/virt-env$ source ./bin/activate #Activate virtual environment
   (virt-env) foo@bar:~/CMakeDoc/virt-env$ pip3 install . #If pip installed
   (virt-env) foo@bar:~/CMakeDoc/virt-env$ python3 setup.py install #If pip not installed

#####
Usage
#####

For each CMake function or variable that you would like to document, prepend it with a block doc-comment.
A block doc-comment begins with :code:`#[[[` and ends with :code:`#]]`.

Then run :code:`cmakedoc` on your CMake files, outputting to a directory of your choosing. The help text is printed below for reference::

   Usage: cmakedoc [-h] [-o OUTPUT] [-r] file [file ...]

   positional arguments:
      file                 CMake file to generate documentation for. If
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

#######
Example
#######

Here we show an example CMake file, called :code:`example.cmake`, that contains
doccomments documenting functions, macros, and variables.
The file contents are shown below.

example.cmake:

.. code:: cmake

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



To generate the documentation, we enter our system shell (example assumes Bash-like shell on a Unix-like system).

Generating documentation in directory :code:`output`:

.. code:: console

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





