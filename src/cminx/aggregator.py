# Copyright 2022 CMakePP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

from .documentation_types import AttributeDocumentation, FunctionDocumentation, MacroDocumentation, \
    VariableDocumentation, GenericCommandDocumentation, ClassDocumentation, TestDocumentation, SectionDocumentation, \
    MethodDocumentation, VarType, CTestDocumentation
from .parser.CMakeListener import CMakeListener
# Annoyingly, the Antl4 Python libraries use camelcase since it was originally Java, so we have convention
# inconsistencies here
from .parser.CMakeParser import CMakeParser
from cminx import Settings

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


class DocumentationAggregator(CMakeListener):
    """
    Processes all docstrings and their associated commands, aggregating
    them in a list.
    """

    def __init__(self, settings: Settings = Settings()):
        self.settings = settings
        """Application settings used to determine what commands to document"""

        self.documented = []
        """All current documented commands"""

        self.documented_classes_stack = []
        """A stack containing the documented classes and inner classes as they are processed"""

        self.documented_awaiting_function_def = None
        """
        A variable containing a documented command such as cpp_member() that is awaiting its function/macro
        definition
        """

        self.consumed = []
        """
        A list containing all of the Command_invocationContexts that have already been processed
        """
        
        self.logger = logging.getLogger(__name__)

    def process_function(self, ctx: CMakeParser.Command_invocationContext, docstring: str):
        """
        Extracts function name and declared parameters.

        :param ctx: Documented command context. Constructed by the Antlr4 parser.

        :param docstring: Cleaned docstring.
        """

        def_params = [param for param in ctx.single_argument()]  # Extract declared function parameters

        if len(def_params) < 1:
            pretty_text = docstring
            pretty_text += f"\n{ctx.getText()}"

            self.logger.error(f"function() called with incorrect parameters: {ctx.single_argument()}\n\n{pretty_text}")
            return

        params = [p.getText() for p in def_params[1:]]
        function_name = def_params[0].getText()

        # Extracts function name and adds the completed function documentation to the 'documented' list
        self.documented.append(FunctionDocumentation(function_name, docstring, params))

    def process_macro(self, ctx: CMakeParser.Command_invocationContext, docstring: str):
        """
        Extracts macro name and declared parameters.

        :param ctx: Documented command context. Constructed by the Antlr4 parser.

        :param docstring: Cleaned docstring.
        """

        def_params = [param for param in ctx.single_argument()]  # Extract declared macro parameters

        if len(def_params) < 1:
            pretty_text = docstring
            pretty_text += f"\n{ctx.getText()}"

            self.logger.error(
                f"macro() called with incorrect parameters: {ctx.single_argument()}\n\n{pretty_text}")
            return

        params = [p.getText() for p in def_params[1:]]
        macro_name = def_params[0].getText()

        # Extracts macro name and adds the completed macro documentation to the 'documented' list
        self.documented.append(MacroDocumentation(macro_name, docstring, params))

    def process_ct_add_test(self, ctx: CMakeParser.Command_invocationContext, docstring: str):
        """
        Extracts test name and declared parameters.

        :param ctx: Documented command context. Constructed by the Antlr4 parser.

        :param docstring: Cleaned docstring.
        """
        params = [param.getText() for param in ctx.single_argument()]  # Extract parameters

        if len(params) < 2:
            pretty_text = docstring
            pretty_text += f"\n{ctx.getText()}"

            self.logger.error(
                f"ct_add_test() called with incorrect parameters: {params}\n\n{pretty_text}")
            return

        name = ""
        expect_fail = False
        for i in range(0, len(params)):
            param = params[i]
            if param.upper() == "NAME":
                try:
                    name = params[i + 1]
                except IndexError:
                    pretty_text = docstring
                    pretty_text += f"\n{ctx.getText()}"

                    self.logger.error(
                        f"ct_add_test() called with incorrect parameters: {params}\n\n{pretty_text}")
                    return

            if param.upper() == "EXPECTFAIL":
                expect_fail = True

        test_doc = TestDocumentation(name, docstring, expect_fail)
        self.documented.append(test_doc)
        self.documented_awaiting_function_def = test_doc

    def process_ct_add_section(self, ctx: CMakeParser.Command_invocationContext, docstring: str):
        """
        Extracts section name and declared parameters.

        :param ctx: Documented command context. Constructed by the Antlr4 parser.

        :param docstring: Cleaned docstring.
        """
        params = [param.getText() for param in ctx.single_argument()]  # Extract parameters

        if len(params) < 2:
            pretty_text = docstring
            pretty_text += f"\n{ctx.getText()}"

            self.logger.error(
                f"ct_add_section() called with incorrect parameters: {params}\n\n{pretty_text}")
            return

        name = ""
        expect_fail = False
        for i in range(0, len(params)):
            param = params[i]
            if param.upper() == "NAME":
                try:
                    name = params[i + 1]
                except IndexError:
                    pretty_text = docstring
                    pretty_text += f"\n{ctx.getText()}"

                    self.logger.error(f"ct_add_section() called with incorrect parameters: {params}\n\n{pretty_text}")
                    return

            if param.upper() == "EXPECTFAIL":
                expect_fail = True

        section_doc = SectionDocumentation(name, docstring, expect_fail)
        self.documented.append(section_doc)
        self.documented_awaiting_function_def = section_doc

    def process_set(self, ctx: CMakeParser.Command_invocationContext, docstring: str):
        """
        Extracts variable name and values from the documented set command.
        Also determines the type of set command/variable: String, List, or Unset.

        :param ctx: Documented command context. Constructed by the Antlr4 parser.

        :param docstring: Cleaned docstring.
        """

        if len(ctx.single_argument()) < 1:
            pretty_text = docstring
            pretty_text += f"\n{ctx.getText()}"

            self.logger.error(
                f"set() called with incorrect parameters: {ctx.single_argument()}\n\n{pretty_text}")
            return

        varname = ctx.single_argument()[
            0].getText()
        # First argument is name of variable so ignore that
        arg_len = len(ctx.single_argument()) - 1

        if arg_len > 1:  # List
            values = [val.getText()
                      for val in ctx.single_argument()[1:]]
            self.documented.append(VariableDocumentation(
                varname, docstring, VarType.LIST, " ".join(values)))
        elif arg_len == 1:  # String
            value = ctx.single_argument()[1].getText()

            # If the value includes the quote marks,
            # need to remove them to get just the raw string
            if value[0] == '"':
                value = value[1:]
            if value[-1] == '"':
                value = value[:-1]
            self.documented.append(VariableDocumentation(
                varname, docstring, VarType.STRING, value))
        else:  # Unset
            self.documented.append(VariableDocumentation(
                varname, docstring, VarType.UNSET, None))

    def process_cpp_class(self, ctx: CMakeParser.Command_invocationContext, docstring: str):
        """
        Extracts the name and the declared superclasses from the documented
        cpp_class command.

        :param ctx: Documented command context. Constructed by the Antlr4 parser.

        :param docstring: Cleaned docstring.
        """

        if len(ctx.single_argument()) < 1:
            pretty_text = docstring
            pretty_text += f"\n{ctx.getText()}"

            self.logger.error(f"cpp_class() called with incorrect parameters: {ctx.single_argument()}\n\n{pretty_text}")
            return

        params = [param.getText()
                  for param in ctx.single_argument()]

        name = params[0]
        superclasses = params[1:]
        clazz = ClassDocumentation(name, docstring, superclasses, [], [], [], [])
        self.documented.append(clazz)

        # If we are currently processing another class, then this one
        # is an inner class and we need to add it
        if len(self.documented_classes_stack) > 0 and self.documented_classes_stack[-1] is not None:
            self.documented_classes_stack[-1].inner_classes.append(clazz)

        # Continue processing within the class's context
        # until we reach cpp_end_class()
        self.documented_classes_stack.append(clazz)

    def process_cpp_member(self, ctx: CMakeParser.Command_invocationContext, docstring: str,
                           is_constructor: bool = False):
        """
        Extracts the method name and declared parameter types from the documented cpp_member
        command.

        :param ctx: Documented command context. Constructed by the Antlr4 parser.

        :param docstring: Cleaned docstring.

        :param is_constructor: Whether the member is a constructor, this parameter is reflected in the generated
        MethodDocumentation.
        """
        if len(ctx.single_argument()) < 2:
            pretty_text = docstring
            pretty_text += f"\n{ctx.getText()}"

            self.logger.error(
                f"cpp_class() called with incorrect parameters: {ctx.single_argument()}\n\n{pretty_text}")
            return

        params = [param.getText()
                  for param in ctx.single_argument()]
        if len(self.documented_classes_stack) <= 0:
            pretty_text = docstring
            pretty_text += f"\n{ctx.getText()}"
            called_type = "cpp_constructor()" if is_constructor else "cpp_member()"

            self.logger.error(
                f"{called_type} called outside of cpp_class() definition: {params}\n\n{pretty_text}")
            return

        clazz = self.documented_classes_stack[-1]
        # Shouldn't document because class isn't supposed to be documented
        if clazz is None:
            return

        parent_class = params[1]
        name = params[0]
        param_types = params[2:] if len(params) > 2 else []
        method_doc = MethodDocumentation(
            name, docstring, parent_class, param_types, [], is_constructor)
        if is_constructor:
            clazz.constructors.append(method_doc)
        else:
            clazz.members.append(method_doc)
        self.documented_awaiting_function_def = method_doc

    def process_cpp_constructor(self, ctx: CMakeParser.Command_invocationContext, docstring: str):
        """
        Alias for calling process_cpp_member() with is_constructor=True.
        """
        self.process_cpp_member(ctx, docstring, is_constructor=True)

    def process_cpp_attr(self, ctx: CMakeParser.Command_invocationContext, docstring: str):
        """
        Extracts the name and any default values from the documented cpp_attr
        command.

        :param ctx: Documented command context. Constructed by the Antlr4 parser.

        :param docstring: Cleaned docstring.
        """
        if len(ctx.single_argument()) < 2:
            pretty_text = docstring
            pretty_text += f"\n{ctx.getText()}"

            self.logger.error(
                f"cpp_attr() called with incorrect parameters: {ctx.single_argument()}\n\n{pretty_text}")
            return

        params = [param.getText()
                  for param in ctx.single_argument()]
        if len(self.documented_classes_stack) <= 0:
            pretty_text = docstring
            pretty_text += f"\n{ctx.getText()}"

            self.logger.error(
                f"cpp_attr() called outside of cpp_class() definition: {params}\n\n{pretty_text}")
            return

        clazz = self.documented_classes_stack[-1]
        # Shouldn't document because class isn't supposed to be documented
        if clazz is None:
            return
        parent_class = params[0]
        name = params[1]
        default_values = params[2] if len(params) > 2 else None
        clazz.attributes.append(AttributeDocumentation(
            name, docstring, parent_class, default_values))

    def process_add_test(self, ctx: CMakeParser.Command_invocationContext, docstring: str):
        """
        Extracts information from a CTest add_test() command.
        Note: this is not the processor for the CMakeTest ct_add_test() command,
        but the processor for the vanilla CMake add_test() command.

        :param ctx: Documented command context. Constructed by the Antlr4 parser.

        :param docstring: Cleaned docstring.
        """
        params = [param.getText() for param in ctx.single_argument()]  # Extract parameters

        if len(params) < 2:
            pretty_text = docstring
            pretty_text += f"\n{ctx.getText()}"

            self.logger.error(
                f"ct_add_section() called with incorrect parameters: {params}\n\n{pretty_text}")
            return

        name = ""
        for i in range(0, len(params)):
            param = params[i]
            if param.upper() == "NAME":
                try:
                    name = params[i + 1]
                except IndexError:
                    pretty_text = docstring
                    pretty_text += f"\n{ctx.getText()}"

                    self.logger.error(f"add_test() called with incorrect parameters: {params}\n\n{pretty_text}")
                    return

        test_doc = CTestDocumentation(name, docstring, filter(lambda p: p != name and p != "NAME", params))
        self.documented.append(test_doc)
        self.documented_awaiting_function_def = test_doc

    def process_generic_command(self, command_name: str, ctx: CMakeParser.Command_invocationContext, docstring: str):
        """
        Extracts command invocation and arguments for a documented command that does not
        have a dedicated processor function.

        :param command_name: The documented command's name, such as add_library.

        :param ctx: Documented command context. Constructed by the Antlr4 parser.

        :param docstring: Cleaned docstring.
        """

        args = ctx.single_argument() + ctx.compound_argument()
        args = [val.getText() for val in args]
        self.documented.append(GenericCommandDocumentation(
            command_name, docstring, args))

    def enterDocumented_command(self, ctx: CMakeParser.Documented_commandContext):
        """
        Main entrypoint into the documentation processor and aggregator. Called by ParseTreeWalker whenever
        encountering a documented command. Cleans the docstring and dispatches ctx to other functions for additional
        processing (process_{command}(), i.e. process_function())

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

        try:
            command = ctx.command_invocation().Identifier().getText().lower()
            self.consumed.append(ctx.command_invocation())
            if f"process_{command}" in dir(self):
                getattr(self, f"process_{command}")(ctx.command_invocation(), cleaned_doc)
            else:
                self.process_generic_command(command, ctx.command_invocation(), cleaned_doc)
        except Exception as e:
            line_num = ctx.command_invocation().start.line
            self.logger.error(
                f"Caught exception while processing documented command beginning at line number {line_num}")
            raise e

    def enterCommand_invocation(self, ctx: CMakeParser.Command_invocationContext):
        """
        Visitor for all other commands, used for locating position-dependent
        elements of documented commands, such as cpp_end_class() that pops the class stack,
        or a function or method definition for cpp_member().
        """

        command = ctx.Identifier().getText().lower()

        try:
            if command == "cpp_class" and not self.settings.input.include_undocumented_cpp_class:
                # This ensures the stack doesn't fall into an inconsistent state
                self.documented_classes_stack.append(None)
            elif command == "cpp_end_class":
                self.documented_classes_stack.pop()
            elif ((command == "function"
                   or command == "macro")
                  and self.documented_awaiting_function_def is not None):
                # We've found the function/macro def that the previous documented command needed
                params = [param.getText()
                          for param in ctx.single_argument()]

                self.documented_awaiting_function_def.is_macro = command == "macro"

                # Ignore function name and self param
                if len(params) > 2:
                    param_names = params[2:]
                    self.documented_awaiting_function_def.params.extend(param_names)

                # Clear the var since we've processed the function/macro def we need
                self.documented_awaiting_function_def = None
            elif command != "set" and f"process_{command}" in dir(self) and ctx not in self.consumed\
                    and self.settings.input.__dict__[f"include_undocumented_{command}"]:
                getattr(self, f"process_{command}")(ctx, "")
        except Exception as e:
            line_num = ctx.start.line
            self.logger.error(f"Caught exception while processing command beginning at line number {line_num}")
            raise e
