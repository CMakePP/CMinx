#!/usr/bin/python3

from cminx.rstwriter import RSTWriter
#from cminx.rst_validator import RSTValidator #No longer in cminx package, included in test/ directory instead as not needed for general operation

if __name__ == "__main__":

    #First we need to build an RSTWriter to validate
    writer = RSTWriter("Title")
    writer.text("This is a test")
    writer.bulleted_list("test", "No")
    writer.enumerated_list(1, "two")
    writer.doctest('print("test")', 'test')
    d = writer.directive("DANGER")
    d.text("This is john")


    #Make a table of values
    tab = [
    [0, 1, 2, 3],
    [4, 5, 6, 7],
    [8, 9, 10, 11]
    ]
    writer.simple_table(tab, column_headings=["Column 1", "Column 2", "Column 3", "Column 4"])


    #Next step is very simple. Just instantiate the validator with your desired settings and the writer
    #Then call validate()
    validator = RSTValidator(writer, werror = True)
    print(validator.validate())
