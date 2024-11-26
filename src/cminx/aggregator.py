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

"""
This module interfaces with the generated CMake parser.
The primary entrypoint is :class:`~DocumentationAggregator`,
which subclasses :class:`cminx.parser.CMakeListener`. This
class listens to all relevent parser rules, generates
:class:`cminx.documentation_types.DocumentationType`
objects that represent the parsed CMake, and
aggregates them in a single list.

:Author: Branden Butler
:License: Apache 2.0
"""
import itertools
import logging
import re
from dataclasses import dataclass
from enum import Enum
from typing import List, Union

from antlr4 import ParserRuleContext

from .documentation_types import AttributeDocumentation, FunctionDocumentation, MacroDocumentation, \
    VariableDocumentation, GenericCommandDocumentation, ClassDocumentation, TestDocumentation, SectionDocumentation, \
    MethodDocumentation, VarType, CTestDocumentation, ModuleDocumentation, AbstractCommandDefinitionDocumentation, \
    OptionDocumentation, DanglingDoccomment, DocumentationType, SetCommandKeywords, CacheVarType

from .exceptions import CMakeSyntaxException
from .parser.CMakeListener import CMakeListener
# Annoyingly, the Antl4 Python libraries use camelcase since it was originally Java, so we have convention
# inconsistencies here
from .parser.CMakeParser import CMakeParser
from cminx import Settings




@dataclass
class DefinitionCommand:
    """
    A container for documentation of definition commands, used to update
    the parameter list when a :code:`cmake_parse_arguments()` command
    is encountered.

    A definition command is a command that defines another command,
    so the function() and macro() commands are definition commands.
    Instances of this dataclass are placed on the top of a stack
    when definition commands are encountered.
    """
    documentation: Union[AbstractCommandDefinitionDocumentation, None]
    """
    The documentation for the definition command. If None,
    this DefinitionCommand will be ignored when popped.
    """

    should_document: bool = True
    """
    Whether the contained documentation object should be updated
    if a :code:`cmake_parse_arguments()` command is found.
    When false, this object is ignored.
    """


class DocumentationAggregator(CMakeListener):
    """
    Processes all docstrings and their associated commands, aggregating
    them in a list. Uses the given :class:`~cminx.config.Settings` object
    to determine aggregation settings, and will document commands without
    doccomments if the associated settings are set.

    The method used to generate the documentation object for
    a given command is chosen by searching for a method with the name
    :code:`"process_<command name>"` with two arguments: :code:`ctx` that is
    of type :class:`cminx.parser.CMakeParser.Command_invocationContext`,
    and :code:`docstring` that is of type string.
    """

    def __init__(self, settings: Settings = Settings()) -> None:
        self.settings: Settings = settings
        """Application settings used to determine what commands to document"""

        self.documented: List[DocumentationType] = []
        """All current documented commands"""

        self.documented_classes_stack: List[Union[ClassDocumentation, None]] = []
        """A stack containing the documented classes and inner classes as they are processed"""

        self.documented_awaiting_function_def: Union[DocumentationType, None] = None
        """
        A variable containing a documented command such as cpp_member() that is awaiting its function/macro
        definition
        """

        self.definition_command_stack: List[DefinitionCommand] = []
        """
        A stack containing the current definition command that we are inside.
        A definition command is any command that defines a construct with both a
        beginning command and an ending command, with all commands within being considered
        part of the definition. Examples of definition commands include
        function(), macro(), and cpp_class().
        """

        self.consumed: List[ParserRuleContext] = []
        """
        A list containing all of the contexts that have already been processed
        """

        self.logger: logging.Logger = logging.getLogger(__name__)

    def process_function(self, ctx: CMakeParser.Command_invocationContext, docstring: str) -> None:
        """
        Extracts function name and declared parameters.

        :param ctx: Documented command context. Constructed by the Antlr4 parser.

        :param docstring: Cleaned docstring.
        """

        def_params = [param for param in ctx.single_argument()]  # Extract declared function parameters

        if len(def_params) < 1:
            pretty_text = docstring
            pretty_text += f"\n{ctx.getText()}"

            raise CMakeSyntaxException(
                f"function() called with incorrect parameters: {ctx.single_argument()}\n\n{pretty_text}",
                ctx.start.line
            )

        params = [
            re.sub(self.settings.input.function_parameter_name_strip_regex, "", p.getText()) for p in def_params[1:]
        ]
        function_name = def_params[0].getText()
        has_kwargs = self.settings.input.kwargs_doc_trigger_string in docstring

        # Extracts function name and adds the completed function documentation to the 'documented' list
        doc = FunctionDocumentation(function_name, docstring, params, has_kwargs)
        self.documented.append(doc)
        self.definition_command_stack.append(DefinitionCommand(doc))

    def process_macro(self, ctx: CMakeParser.Command_invocationContext, docstring: str) -> None:
        """
        Extracts macro name and declared parameters.

        :param ctx: Documented command context. Constructed by the Antlr4 parser.

        :param docstring: Cleaned docstring.
        """

        def_params = [param for param in ctx.single_argument()]  # Extract declared macro parameters

        if len(def_params) < 1:
            pretty_text = docstring
            pretty_text += f"\n{ctx.getText()}"

            raise CMakeSyntaxException(
                f"macro() called with incorrect parameters: {ctx.single_argument()}\n\n{pretty_text}",
                ctx.start.line
            )

        params = [
            re.sub(self.settings.input.macro_parameter_name_strip_regex, "", p.getText()) for p in def_params[1:]
        ]
        macro_name = def_params[0].getText()
        has_kwargs = self.settings.input.kwargs_doc_trigger_string in docstring

        # Extracts macro name and adds the completed macro documentation to the 'documented' list
        doc = MacroDocumentation(macro_name, docstring, params, has_kwargs)
        self.documented.append(doc)
        self.definition_command_stack.append(DefinitionCommand(doc))

    def process_cmake_parse_arguments(self, ctx: CMakeParser.Command_invocationContext, docstring: str) -> None:
        """
        Determines whether a documented function or macro uses *args or *kwargs.
        Accesses the last element in the :code:`definition_command_stack` to
        update the documentation's :code:`has_kwargs` field.

        :param ctx: Documented command context. Constructed by the Antlr4 parser.

        :param docstring: Cleaned docstring.
        """
        if len(self.definition_command_stack) > 0:
            last_element = self.definition_command_stack[-1]
            if last_element.should_document and isinstance(last_element.documentation,
                                                           AbstractCommandDefinitionDocumentation):
                last_element.documentation.has_kwargs = True

    def process_ct_add_test(self, ctx: CMakeParser.Command_invocationContext, docstring: str) -> None:
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

    def process_ct_add_section(self, ctx: CMakeParser.Command_invocationContext, docstring: str) -> None:
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

    def process_set(self, ctx: CMakeParser.Command_invocationContext, docstring: str) -> None:
        """
        Extracts variable name and values from the documented set command.
        Also determines the type of set command/variable: String, List, or Unset.

        :param ctx: Documented command context. Constructed by the Antlr4 parser.

        :param docstring: Cleaned docstring.
        """
        params = [val.getText() for val in ctx.single_argument()]
        if len(ctx.single_argument()) < 1:
            pretty_text = docstring
            pretty_text += f"\n{ctx.getText()}"

            self.logger.error(
                f"set() called with incorrect parameters: {ctx.single_argument()}\n\n{pretty_text}")
            return

        varname = params[0]
        # Used for comparing against the set() command's keywords
        params_upper = [param.upper() for param in params[1:]]
        values = list(
            itertools.takewhile(
                lambda param: param not in SetCommandKeywords.values(),
                params[1:]
            )
        )

        keywords = {kw: kw.value in params_upper for kw in SetCommandKeywords}

        if keywords[SetCommandKeywords.CACHE]:
            cache_keyword_index = params.index(SetCommandKeywords.CACHE.value)
            cache_var_type = CacheVarType.values()[params[cache_keyword_index + 1]]
            cache_var_docstring = params[cache_keyword_index + 2]
        else:
            cache_var_type = None
            cache_var_docstring = ""

        if len(values) > 1:  # List
            self.documented.append(VariableDocumentation(
                varname, docstring, VarType.LIST, " ".join(values), keywords, cache_var_type, cache_var_docstring
            ))
        elif len(values) == 1:  # String
            value = ctx.single_argument()[1].getText()

            # If the value includes the quote marks,
            # need to remove them to get just the raw string
            if value[0] == '"':
                value = value[1:]
            if value[-1] == '"':
                value = value[:-1]
            self.documented.append(VariableDocumentation(
                varname, docstring, VarType.STRING, value, keywords, cache_var_type, cache_var_docstring
            ))
        else:  # Unset
            self.documented.append(VariableDocumentation(
                varname, docstring, VarType.UNSET, None, keywords
            ))

    def process_cpp_class(self, ctx: CMakeParser.Command_invocationContext, docstring: str) -> None:
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
                           is_constructor: bool = False) -> None:
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

    def process_cpp_constructor(self, ctx: CMakeParser.Command_invocationContext, docstring: str) -> None:
        """
        Alias for calling process_cpp_member() with is_constructor=True.
        """
        self.process_cpp_member(ctx, docstring, is_constructor=True)

    def process_cpp_attr(self, ctx: CMakeParser.Command_invocationContext, docstring: str) -> None:
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

    def process_add_test(self, ctx: CMakeParser.Command_invocationContext, docstring: str) -> None:
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

        test_doc = CTestDocumentation(name, docstring, [p for p in params if p != name and p != "NAME"])
        self.documented.append(test_doc)

    def process_option(self, ctx: CMakeParser.Command_invocationContext, docstring: str) -> None:
        """
        Extracts information from an :code:`option()` command and creates
        an OptionDocumentation from it. It extracts the option name,
        the help text, and the default value if any.

        :param ctx: Documented command context. Constructed by the Antlr4 parser.
        :param docstring: Cleaned docstring.
        """
        params = [param.getText() for param in ctx.single_argument()]  # Extract parameters
        if len(params) < 2 or len(params) > 3:
            pretty_text = docstring
            pretty_text += f"\n{ctx.getText()}"

            self.logger.error(
                f"option() called with incorrect parameters: {params}\n\n{pretty_text}")
            return

        option_doc = OptionDocumentation(
            params[0],
            docstring,
            "bool",
            params[2] if len(params) == 3 else None,
            {},
            None,
            params[1]
        )
        self.documented.append(option_doc)

    def process_generic_command(self, command_name: str, ctx: CMakeParser.Command_invocationContext,
                                docstring: str) -> None:
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

    @staticmethod
    def clean_doc_lines(lines: List[str]) -> str:
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

        return cleaned_doc

    def enterDocumented_command(self, ctx: CMakeParser.Documented_commandContext) -> None:
        """
        Main entrypoint into the documentation processor and aggregator. Called by ParseTreeWalker whenever
        encountering a documented command. Cleans the docstring and dispatches ctx to other functions for additional
        processing (process_{command}(), i.e. process_function())

        :param ctx: Documented command context, constructed by the Antlr4 parser.

        :raise NotImplementedError: If no processor can be found for the command that was documented.
        """
        self.consumed.append(ctx.bracket_doccomment())
        text = ctx.bracket_doccomment().getText()
        lines = text.split("\n")

        cleaned_doc = DocumentationAggregator.clean_doc_lines(lines)

        try:
            command = ctx.command_invocation().Identifier().getText().lower()
            self.consumed.append(ctx.command_invocation())
            self.consumed.append(ctx.bracket_doccomment())
            if f"process_{command}" in dir(self):
                getattr(self, f"process_{command}")(ctx.command_invocation(), cleaned_doc)
            else:
                self.process_generic_command(command, ctx.command_invocation(), cleaned_doc)
        except Exception as e:
            line_num = ctx.command_invocation().start.line
            self.logger.error(
                f"Caught exception while processing documented command beginning at line number {line_num}"
            )
            raise e

    def enterCommand_invocation(self, ctx: CMakeParser.Command_invocationContext) -> None:
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
            elif command == "cmake_parse_arguments":
                self.process_cmake_parse_arguments(ctx, "")
            elif ((command == "function"
                   or command == "macro")
                  and self.documented_awaiting_function_def is not None):
                # We've found the function/macro def that the previous documented command needed
                params = [param.getText()
                          for param in ctx.single_argument()]
                if isinstance(self.documented_awaiting_function_def, MethodDocumentation):
                    params = [
                        re.sub(self.settings.input.member_parameter_name_strip_regex, "", p.getText()) for p in
                        ctx.single_argument()
                    ]

                self.documented_awaiting_function_def.is_macro = command == "macro"

                # Ignore function name and self param
                if len(params) > 2:
                    param_names = params[2:]
                    self.documented_awaiting_function_def.params.extend(param_names)

                # Clear the var since we've processed the function/macro def we need
                self.documented_awaiting_function_def = None

                # Allows scanning for cmake_parse_arguments() inside other types of definitions
                self.definition_command_stack.append(DefinitionCommand(None, False))
            elif command == "endfunction" or command == "endmacro":
                self.definition_command_stack.pop()
            elif command != "set" and f"process_{command}" in dir(self) and ctx not in self.consumed:
                if self.settings.input.__dict__[f"include_undocumented_{command}"]:
                    getattr(self, f"process_{command}")(ctx, "")
                elif command == "function" or command == "macro":
                    self.definition_command_stack.append(DefinitionCommand(None, False))

        except Exception as e:
            line_num = ctx.start.line
            self.logger.error(f"Caught exception while processing command beginning at line number {line_num}")
            raise e

    def enterDocumented_module(self, ctx: CMakeParser.Documented_moduleContext) -> None:
        text = ctx.Module_docstring().getText()
        cleaned_lines = DocumentationAggregator.clean_doc_lines(text.split("\n")).split("\n")
        module_name = cleaned_lines[0].replace("@module", "").strip()
        doc = "\n".join(cleaned_lines[1:])
        self.documented.append(ModuleDocumentation(module_name, doc))

    def enterBracket_doccomment(self, ctx: CMakeParser.Bracket_doccommentContext) -> None:
        if ctx not in self.consumed:
            # text = ctx.Docstring().getText()
            # cleaned_lines = DocumentationAggregator.clean_doc_lines(text.split("\n")).split("\n")
            # self.documented.append(DanglingDoccomment("", "\n".join(cleaned_lines)))
            self.logger.warning(
                f"Detected dangling doccomment, ignoring. RST may change depending on CMinx version."
            )
