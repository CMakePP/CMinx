import sys

from antlr4 import *  # FIXME Remove unused imports
from enum import Enum
from collections import namedtuple

# Annoyingly, the Antl4 Python libraries use camelcase since it was originally Java, so we have convention inconsistencies here
from .CMakeParser import CMakeParser
from .CMakeListener import CMakeListener


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


FunctionDocumentation = namedtuple(
    'FunctionDocumentation', 'function params doc')
MacroDocumentation = namedtuple("MacroDocumentation", "macro params doc")
VariableDocumentation = namedtuple(
    'VariableDocumentation', 'varname type value doc')
TestDocumentation = namedtuple('TestDocumentation', 'name expect_fail doc')
SectionDocumentation = namedtuple(
    'SectionDocumentation', 'name expect_fail doc')
GenericCommandDocumentation = namedtuple(
    'GenericCommandDocumentation', 'name params doc')
ClassDocumentation = namedtuple(
    'ClassDocumentation', 'name superclasses inner_classes members doc')
AttributeDocumentation = namedtuple(
    'ClassDocumentation', 'parent_class name default_value doc')

class MethodDocumentation:
    def __init__(self, parent_class, name, param_types, doc) -> None:
        self.parent_class = parent_class
        self.name = name
        self.param_types = param_types
        self.params = []
        self.doc = doc
# MethodDocumentation = namedtuple(
#     'MethodDocumentation', 'parent_class name param_types params doc')

DOC_TYPES = (FunctionDocumentation, MacroDocumentation, VariableDocumentation,
             TestDocumentation, SectionDocumentation, GenericCommandDocumentation,
             ClassDocumentation, AttributeDocumentation)

VarType = Enum("VarType", "String List Unset")


class DocumentationAggregator(CMakeListener):
    """
    Processes all docstrings and their associated commands, aggregating
    them in a list.
    """

    def __init__(self):
        self.documented = []
        """All current documented commands"""

        self.documented_classes_stack = []
        """A stack containing the documented classes and inner classes as they are processed"""

        self.documented_awaiting_function_def = None
        """
        A variable containing a documented command such as cpp_member() that is awaiting its function/macro
        definition
        """

    def process_function(self, ctx: CMakeParser.Documented_commandContext, docstring: str):
        """
        Extracts function name and declared parameters.

        :param ctx: Documented command context. Constructed by the Antlr4 parser.

        :param docstring: Cleaned docstring.
        """
        params = [param.Identifier().getText() for param in ctx.command_invocation(
        ).single_argument()[1:]]  # Extract declared function parameters
        self.documented.append(FunctionDocumentation(ctx.command_invocation().single_argument()[0].Identifier().getText(
        ), params, docstring))  # Extracts function name and adds the completed function documentation to the 'documented' list

    def process_macro(self, ctx: CMakeParser.Documented_commandContext, docstring: str):
        """
        Extracts macro name and declared parameters.

        :param ctx: Documented command context. Constructed by the Antlr4 parser.

        :param docstring: Cleaned docstring.
        """
        params = [param.Identifier().getText() for param in ctx.command_invocation(
        ).single_argument()[1:]]  # Extract declared macro parameters
        self.documented.append(MacroDocumentation(ctx.command_invocation().single_argument()[0].Identifier().getText(
        ), params, docstring))  # Extracts macro name and adds the completed macro documentation to the 'documented' list

    def process_ct_add_test(self, ctx: CMakeParser.Documented_commandContext, docstring: str):
        """
        Extracts test name and declared parameters.

        :param ctx: Documented command context. Constructed by the Antlr4 parser.

        :param docstring: Cleaned docstring.
        """
        params = [param.Identifier().getText() for param in ctx.command_invocation(
        ).single_argument()]  # Extract parameters
        name = ""
        expect_fail = False
        for i in range(0, len(params)):
            param = params[i]
            if param.upper() == "NAME":
                try:
                    name = params[i + 1]
                except IndexError:
                    pretty_text = '\n'.join(
                        ctx.Bracket_doccomment().getText().split('\n'))
                    pretty_text += f"\n{ctx.command_invocation().getText()}"

                    print(
                        f"ct_add_test() called with incorrect parameters: {params}\n\n{pretty_text}", file=sys.stderr)
                    return

            if param.upper() == "EXPECTFAIL":
                expect_fail = True

        self.documented.append(TestDocumentation(name, expect_fail, docstring))

    def process_ct_add_section(self, ctx: CMakeParser.Documented_commandContext, docstring: str):
        """
        Extracts section name and declared parameters.

        :param ctx: Documented command context. Constructed by the Antlr4 parser.

        :param docstring: Cleaned docstring.
        """
        params = [param.Identifier().getText() for param in ctx.command_invocation(
        ).single_argument()]  # Extract parameters
        name = ""
        expect_fail = False
        for i in range(0, len(params)):
            param = params[i]
            if param.upper() == "NAME":
                try:
                    name = params[i + 1]
                except IndexError:
                    pretty_text = '\n'.join(
                        ctx.Bracket_doccomment().getText().split('\n'))
                    pretty_text += f"\n{ctx.command_invocation().getText()}"

                    print(
                        f"ct_add_section() called with incorrect parameters: {params}\n\n{pretty_text}", file=sys.stderr)
                    return

            if param.upper() == "EXPECTFAIL":
                expect_fail = True

        self.documented.append(SectionDocumentation(
            name, expect_fail, docstring))

    def process_set(self, ctx: CMakeParser.Documented_commandContext, docstring: str):
        """
        Extracts variable name and values from the documented set command.
        Also determines the type of set command/variable: String, List, or Unset.

        :param ctx: Documented command context. Constructed by the Antlr4 parser.

        :param docstring: Cleaned docstring.
        """
        varname = ctx.command_invocation().single_argument()[
            0].Identifier().getText()
        # First argument is name of variable so ignore that
        arg_len = len(ctx.command_invocation().single_argument()) - 1

        if arg_len > 1:  # List
            values = [val.getText()
                      for val in ctx.command_invocation().single_argument()[1:]]
            self.documented.append(VariableDocumentation(
                varname, VarType.List, values, docstring))
        elif arg_len == 1:  # String
            value = ctx.command_invocation().single_argument()[1].getText()

            # Includes the quote marks, need to remove them to get just the raw string
            if value[0] == '"':
                value = value[1:]
            if value[-1] == '"':
                value = value[:-1]
            self.documented.append(VariableDocumentation(
                varname, VarType.String, value, docstring))
        else:  # Unset
            self.documented.append(VariableDocumentation(
                varname, VarType.Unset, None, docstring))

    def process_cpp_class(self, ctx: CMakeParser.Documented_commandContext, docstring: str):
        """
        Extracts the name and the declared superclasses from the documented
        cpp_class command.

        :param ctx: Documented command context. Constructed by the Antlr4 parser.

        :param docstring: Cleaned docstring.
        """

        params = [param.Identifier().getText()
                  for param in ctx.command_invocation().single_argument()]
        try:
            name = params[0]
            superclasses = params[1:]
            clazz = ClassDocumentation(name, superclasses, [], [], docstring)
            self.documented.append(clazz)
            if len(self.documented_classes_stack) > 0:
                self.documented_classes_stack[-1].inner_classes.append(clazz)
            self.documented_classes_stack.append(clazz)

        except IndexError:
            pretty_text = '\n'.join(
                ctx.Bracket_doccomment().getText().split('\n'))
            pretty_text += f"\n{ctx.command_invocation().getText()}"

            print(
                f"cpp_class() called with incorrect parameters: {params}\n\n{pretty_text}", file=sys.stderr)
            return

    def process_cpp_member(self, ctx: CMakeParser.Documented_commandContext, docstring: str):
        """
        Extracts the method name and declared parameter types from the documented cpp_member
        command.

        :param ctx: Documented command context. Constructed by the Antlr4 parser.

        :param docstring: Cleaned docstring.
        """
        params = [param.getText()
                  for param in ctx.command_invocation().single_argument()]
        if len(self.documented_classes_stack) <= 0:
            pretty_text = '\n'.join(
                ctx.Bracket_doccomment().getText().split('\n'))
            pretty_text += f"\n{ctx.command_invocation().getText()}"

            print(
                f"cpp_attr() called outside of cpp_class() definition: {params}\n\n{pretty_text}", file=sys.stderr)
            return

        clazz = self.documented_classes_stack[-1]
        try:
            parent_class = params[1]
            name = params[0]
            param_types = params[2:] if len(params) > 2 else None
            method_doc = MethodDocumentation(
                parent_class, name, param_types, docstring)
            clazz.members.append(method_doc)
            self.documented_awaiting_function_def = method_doc
        except IndexError:
            pretty_text = '\n'.join(
                ctx.Bracket_doccomment().getText().split('\n'))
            pretty_text += f"\n{ctx.command_invocation().getText()}"

            print(
                f"cpp_attr() called with incorrect parameters: {params}\n\n{pretty_text}", file=sys.stderr)
            return
        

    def process_cpp_attr(self, ctx: CMakeParser.Documented_commandContext, docstring: str):
        """
        Extracts the name and any default values from the documented cpp_attr
        command.

        :param ctx: Documented command context. Constructed by the Antlr4 parser.

        :param docstring: Cleaned docstring.
        """
        params = [param.getText()
                  for param in ctx.command_invocation().single_argument()]
        if len(self.documented_classes_stack) <= 0:
            pretty_text = '\n'.join(
                ctx.Bracket_doccomment().getText().split('\n'))
            pretty_text += f"\n{ctx.command_invocation().getText()}"

            print(
                f"cpp_attr() called outside of cpp_class() definition: {params}\n\n{pretty_text}", file=sys.stderr)
            return

        clazz = self.documented_classes_stack[-1]
        try:
            parent_class = params[0]
            name = params[1]
            default_values = params[2] if len(params) > 2 else None
            clazz.members.append(AttributeDocumentation(
                parent_class, name, default_values, docstring))
        except IndexError:
            pretty_text = '\n'.join(
                ctx.Bracket_doccomment().getText().split('\n'))
            pretty_text += f"\n{ctx.command_invocation().getText()}"

            print(
                f"cpp_attr() called with incorrect parameters: {params}\n\n{pretty_text}", file=sys.stderr)
            return

    def process_generic_command(self, command_name: str, ctx: CMakeParser.Documented_commandContext, docstring: str):
        """
        Extracts command invocation and arguments for a documented command that does not
        have a dedicated processor function.

        :param command_name: The documented command's name, such as add_library.

        :param ctx: Documented command context. Constructed by the Antlr4 parser.

        :param docstring: Cleaned docstring.
        """

        args = ctx.command_invocation().single_argument(
        ) + ctx.command_invocation().compound_argument()
        args = [val.getText() for val in args]
        self.documented.append(GenericCommandDocumentation(
            command_name, args, docstring))

    def enterDocumented_command(self, ctx: CMakeParser.Documented_commandContext):
        """
        Main entrypoint into the documentation processor and aggregator. Called by ParseTreeWalker whenever encountering a documented command.
        Cleans the docstring and dispatches ctx to other functions for additional processing (process_{command}(), i.e. process_function())

        :param ctx: Documented command context, constructed by the Antlr4 parser.

        :raise NotImplementedError: If no processor can be found for the command that was documented.
        """
        text = ctx.Bracket_doccomment().getText()
        lines = text.split("\n")

        # If last line starts with leading spaces or tabs, count how many and remove from all lines
        num_spaces = 0
        for i in range(0, len(lines[-1])):
            if lines[-1][i] != "#":
                num_spaces = num_spaces + 1
            else:
                break

        cleaned_lines = []
        for line in lines:
            # Remove global indent from left side
            cleaned_line = line[num_spaces:]
            # Remove all hash marks and brackets from the left side only
            cleaned_line = cleaned_line.lstrip("#[]")
            # String is not empty and first character is a space
            if cleaned_line and cleaned_line[0] == " ":
                # Cleans optional singular space
                cleaned_line = cleaned_line[1:]
            cleaned_lines.append(cleaned_line)
        cleaned_lines[-1] = cleaned_lines[-1].rstrip("#]")
        cleaned_doc = "\n".join(cleaned_lines)
        if cleaned_doc.startswith("\n"):
            cleaned_doc = cleaned_doc[1:]
        command = ctx.command_invocation().Identifier().getText().lower()
        if command == "cpp_end_class":
            self.documented_classes_stack.pop()
        if f"process_{command}" in dir(self):
            getattr(self, f"process_{command}")(ctx, cleaned_doc)
        else:
            self.process_generic_command(command, ctx, cleaned_doc)

    def enterCommand_invocation(self, ctx: CMakeParser.Command_invocationContext):
        if ctx.Identifier().getText().lower() == "cpp_end_class":
            self.documented_classes_stack.pop()
        elif ((ctx.Identifier().getText().lower() == "function"
            or ctx.Identifier().getText().lower() == "macro")
            and self.documented_awaiting_function_def is not None):
            #We've found the function/macro def that the previous documented command needed
            params = [param.getText()
                  for param in ctx.single_argument()]
            #Ignore function name and self param
            if len(params) > 2:
                param_names = params[2:]
                self.documented_awaiting_function_def.params = param_names

            #Clear the var since we've processed the function/macro def we need
            self.documented_awaiting_function_def = None
