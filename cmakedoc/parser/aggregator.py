#!/usr/bin/python3
import sys
from antlr4 import *
from enum import Enum
from collections import namedtuple

from .CMakeLexer import CMakeLexer
from .CMakeParser import CMakeParser
from .CMakeListener import CMakeListener

FunctionDocumentation = namedtuple('FunctionDocumentation', 'function params doc')

VariableDocumentation = namedtuple('VariableDocumentation', 'varname type value doc')
VarType = Enum("VarType", "String List Unset")

class DocumentationAggregator(CMakeListener):
    """
    Processes all docstrings and their associated commands, aggregating them in a list.
    """


    def __init__(self):
         self.documented = []
         """All current documented commands"""

    def process_function(self, ctx:CMakeParser.Documented_commandContext, docstring):
         """
         Extracts function name and declared parameters
         """
         params = [param.Identifier().getText() for param in ctx.command_invocation().single_argument()[1:]] #Extract declared function parameters
         self.documented.append(FunctionDocumentation(ctx.command_invocation().single_argument()[0].Identifier().getText(), params, docstring))

    def process_set(self, ctx:CMakeParser.Documented_commandContext, docstring):
        """
        Extracts variable name and values from the documented set command.
        Also determines the type of set command/variable: String, List, or Unset.
        """
        varname = ctx.command_invocation().single_argument()[0].Identifier().getText()
        arg_len = len(ctx.command_invocation().single_argument()) - 1 #First argument is name of variable so ignore that

        if arg_len > 1: #List
             values = [val.getText() for val in ctx.command_invocation().single_argument()[1:]]
             self.documented.append(VariableDocumentation(varname, VarType.List, values, docstring))
        elif arg_len > 1: #String
             value = ctx.command_invocation().single_argument()[1].getText()
             self.documented.append(VariableDocumentation(varname, VarType.String, value, docstring))
        else: #Unset
             self.documented.append(VariableDocumentation(varname, VarType.Unset, None, docstring))

    def enterDocumented_command(self, ctx:CMakeParser.Documented_commandContext):
         """
         Main entrypoint into the documentation processor and aggregator. Called by ParseTreeWalker whenever encountering a documented command.
         Cleans the docstring and dispatches ctx to other functions for additional processing.
         """
         text = ctx.Bracket_doccomment().getText()
         lines = text.split("\n")
         cleaned_lines = []
         for line in lines:
              cleaned_line = line.lstrip("#[]") #Remove all hash marks and brackets from the left side only
              if cleaned_line and cleaned_line[0] == " ": #String is not empty and first character is a space
                   cleaned_line = cleaned_line[1:] #Cleans optional singular space
              cleaned_lines.append(cleaned_line)
         cleaned_doc = "\n".join(cleaned_lines)
         command = ctx.command_invocation().Identifier().getText().lower()
         if f"process_{command}" in dir(self):
              getattr(self, f"process_{command}")(ctx, cleaned_doc)
         else:
              pretty_text = '\n'.join(ctx.Bracket_doccomment().getText().split('\n'))
              pretty_text += f"\n{ctx.command_invocation().getText()}"
              raise NotImplementedError(f"Documentation cannot be generated for:\n{pretty_text}")

