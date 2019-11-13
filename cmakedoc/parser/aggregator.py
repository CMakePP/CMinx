"""
This module interfaces with the generated CMake parser.
It also subclasses CMakeListener to aggregate and further
process documented commands on-the-fly.

Processed documentation is stored in two different types of named tuples
depending on the type being documented. VariableDocumentation also stores
what type the variable is, either String or List for most purposes but also
supports Unset in case someone wants to document why something is unset.

:Author: Branden Butler
:License: Apache 2.0
"""


from antlr4 import * #FIXME Remove unused imports
from enum import Enum
from collections import namedtuple


#Annoyingly, the Antl4 Python libraries use camelcase since it was originally Java, so we have convention inconsistencies here
from .CMakeParser import CMakeParser
from .CMakeListener import CMakeListener

FunctionDocumentation = namedtuple('FunctionDocumentation', 'function params doc')
MacroDocumentation = namedtuple("MacroDocumentation", "macro params doc")
VariableDocumentation = namedtuple('VariableDocumentation', 'varname type value doc')


VarType = Enum("VarType", "String List Unset")

class DocumentationAggregator(CMakeListener):
    """
    Processes all docstrings and their associated commands, aggregating them in a list.
    """


    def __init__(self):
         self.documented = []
         """All current documented commands"""

    def process_function(self, ctx:CMakeParser.Documented_commandContext, docstring: str):
         """
         Extracts function name and declared parameters.

         :param ctx: Documented command context. Constructed by the Antlr4 parser.

         :param docstring: Cleaned docstring.
         """
         params = [param.Identifier().getText() for param in ctx.command_invocation().single_argument()[1:]] #Extract declared function parameters
         self.documented.append(FunctionDocumentation(ctx.command_invocation().single_argument()[0].Identifier().getText(), params, docstring)) #Extracts function name and adds the completed function documentation to the 'documented' list

    def process_macro(self, ctx:CMakeParser.Documented_commandContext, docstring: str):
         """
         Extracts macro name and declared parameters.

         :param ctx: Documented command context. Constructed by the Antlr4 parser.

         :param docstring: Cleaned docstring.
         """
         params = [param.Identifier().getText() for param in ctx.command_invocation().single_argument()[1:]] #Extract declared macro parameters
         self.documented.append(MacroDocumentation(ctx.command_invocation().single_argument()[0].Identifier().getText(), params, docstring)) #Extracts macro name and adds the completed macro documentation to the 'documented' list

    def process_set(self, ctx:CMakeParser.Documented_commandContext, docstring: str):
        """
        Extracts variable name and values from the documented set command.
        Also determines the type of set command/variable: String, List, or Unset.

        :param ctx: Documented command context. Constructed by the Antlr4 parser.

        :param docstring: Cleaned docstring.
        """
        varname = ctx.command_invocation().single_argument()[0].Identifier().getText()
        arg_len = len(ctx.command_invocation().single_argument()) - 1 #First argument is name of variable so ignore that

        if arg_len > 1: #List
             values = [val.getText() for val in ctx.command_invocation().single_argument()[1:]]
             self.documented.append(VariableDocumentation(varname, VarType.List, values, docstring))
        elif arg_len == 1: #String
             value = ctx.command_invocation().single_argument()[1].getText()
             self.documented.append(VariableDocumentation(varname, VarType.String, value, docstring))
        else: #Unset
             self.documented.append(VariableDocumentation(varname, VarType.Unset, None, docstring))

    def enterDocumented_command(self, ctx:CMakeParser.Documented_commandContext):
         """
         Main entrypoint into the documentation processor and aggregator. Called by ParseTreeWalker whenever encountering a documented command.
         Cleans the docstring and dispatches ctx to other functions for additional processing (process_{command}(), i.e. process_function())

         :param ctx: Documented command context, constructed by the Antlr4 parser.

         :raise NotImplementedError: If no processor can be found for the command that was documented.
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

