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
This module contains a large assortment of dataclasses
that represent each of the different types of documented
commands that CMinx recognizes. Each dataclass also implements
an abstract :code:`process()` method to convert the dataclass
representation into an RST representation using :class:`RSTWriter`.

:Author: Branden Butler
:License: Apache 2.0

"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Union, List

from . import Settings
from .rstwriter import RSTWriter, Directive, interpreted_text


class VarType(Enum):
    """The types of variables accepted by the CMake :code:`set()` command"""
    
    STRING = 1
    LIST = 2
    UNSET = 3


@dataclass
class DocumentationType(ABC):
    """
    This is the base class for all documentation types. It defines a single
    abstract process() method that is used to write the documentation RST
    to a given :class:`RSTWriter`.
    """
    name: str
    """The name of the documentation type. For functions this is the function
    name, for variables this is the variable name, etc."""

    doc: str
    """The full doc comment, cleaned of # characters."""

    @abstractmethod
    def process(self, writer: RSTWriter):
        """
        Processes the data stored in this documentation type,
        converting it to RST form by using the given RST writer.

        :param writer: RSTWriter instance that the documentation
        will be added to.
        """
        pass


@dataclass
class AbstractCommandDefinitionDocumentation(DocumentationType, ABC):
    """
    Abstract dataclass that acts as the parent of FunctionDocumentation
    and MacroDocumentation.
    """

    params: List[str]
    """The list of parameters a command definition takes"""

    has_kwargs: bool = False
    """Whether this command definition has keyword arguments."""


@dataclass
class FunctionDocumentation(AbstractCommandDefinitionDocumentation):
    """
    This class serves as the representation of a documented
    CMake function definition. It converts the function definition
    directly to a Sphinx :code:`function` directive.
    """

    def process(self, writer: RSTWriter):
        param_list = self.params
        if self.has_kwargs:
            param_list.append("**kwargs")
        d = writer.directive(
            "function", f"{self.name}({' '.join(param_list)})")
        d.text(self.doc)


@dataclass
class MacroDocumentation(AbstractCommandDefinitionDocumentation):
    """
    This class serves as the representation of a documented
    CMake macro definition. It converts the macro definition
    directly to a Sphinx :code:`function` directive and adds a
    :code:`note` directive specifying that it is a macro.
    """

    def process(self, writer: RSTWriter):
        param_list = self.params
        if self.has_kwargs:
            param_list.append("**kwargs")
        d = writer.directive(
            "function", f"{self.name}({' '.join(param_list)})")
        d.directive(
            "note",
            "This is a macro, and so does not introduce a new scope.")
        d.text(self.doc)


@dataclass
class VariableDocumentation(DocumentationType):
    """
    This class serves as the representation of a documented
    CMake variable definition (:code:`set()` command). It can only
    recognize the CMake primitives :code:`str` and :code:`list`, as
    well as the :code:`UNSET` subcommand.

    This class translates the definition into a Sphinx
    :code:`data` directive, with a :code:`Default value` field
    and a :code:`type` field.
    """

    type: Union[VarType, str]
    """The type that the variable is."""

    value: Union[str, None]
    """A default value that the variable has"""

    def process(self, writer: RSTWriter):
        d = writer.directive("data", f"{self.name}")
        d.text(self.doc)
        d.field("Default value", self.value)
        if self.type == VarType.STRING:
            var_type = "str"
        elif self.type == VarType.LIST:
            var_type = "list"
        elif self.type == VarType.UNSET:
            var_type = "UNSET"
        else:
            raise ValueError(f"Unknown variable type: {self.type}")
        d.field("type", var_type)


@dataclass
class OptionDocumentation(VariableDocumentation):
    """
    This class documents a CMake option() command,
    representing a user-configurable option that can
    be selected via the cache. The RST form of this documentation
    also uses the :code:`data` directive, but includes a note
    specifying the variable is an option.
    """

    help_text: str
    """The help text that the option has."""

    def process(self, writer: RSTWriter):
        d = writer.directive("data", f"{self.name}")
        note = d.directive("note")
        note.text(
            f"""
            This variable is a user-editable option,
            meaning it appears within the cache and can be
            edited on the command line by the :code:`-D` flag.
            """)
        d.text(self.doc)
        d.field("Help text", self.help_text)
        d.field("Default value", self.value if self.value is not None else "OFF")
        d.field("type", self.type)


@dataclass
class GenericCommandDocumentation(DocumentationType):
    """
    This class represents any documented command that does
    not fit into any of the other documentation types.

    All this class does is translate the documented
    command into a Sphinx :code:`function` directive with
    a warning that it is a command invocation and not
    a definition.
    """

    params: List[str]
    """Any parameters passed to the command, unfiltered since this documentation type has no knowledge of the command"""

    def process(self, writer: RSTWriter):
        d = writer.directive(
            "function", f"{self.name}({' '.join(self.params)})")
        d.directive(
            "warning",
            "This is a generic command invocation. It is not a function or macro definition.")
        d.text(self.doc)


@dataclass
class CTestDocumentation(DocumentationType):
    """
    This dataclass holds documentation information
    for a vanilla CTest test. These tests are created
    with the "add_test()" command from regular
    CMake, and documenting such a call will
    create this type of documentation.
    """
    params: List[str] = field(default_factory=lambda: [])

    def process(self, writer: RSTWriter):
        d = writer.directive(
            "function",
            f"{self.name}({' '.join(self.params)})")
        d.directive(
            "warning",
            'This is a CTest test definition, do not call this manually. '
            'Use the "ctest" program to execute this test.')
        d.text(self.doc)


@dataclass
class TestDocumentation(DocumentationType):
    """
    This class provides support for documenting
    CMakeTest tests. It translates the test definition
    into a Sphinx :code:`function` definition with an
    EXPECTFAIL parameter if the test is expected to fail
    and a warning stating that it is a test and should not
    be called manually.
    """

    expect_fail: bool
    """Whether this test expects to fail."""

    params: List[str] = field(default_factory=lambda: [])
    """Any parameters defined by the linked function."""

    is_macro: bool = False
    """Whether the linked command is a macro or a function. If true, a warning stating so is generated."""

    def process(self, writer: RSTWriter):
        d = writer.directive(
            "function",
            f"{self.name}({'EXPECTFAIL' if self.expect_fail else ''})")
        d.directive(
            "warning",
            "This is a CMakeTest test definition, do not call this manually.")
        d.text(self.doc)


@dataclass
class SectionDocumentation(TestDocumentation):
    """
    This class provides support for documenting
    CMakeTest test sections. It translates the
    section exactly as :class:`TestDocumentation`
    except that the warning says that it is a test
    section.
    """

    def process(self, writer: RSTWriter):
        d = writer.directive(
            "function",
            f"{self.name}({'EXPECTFAIL' if self.expect_fail else ''})")
        d.directive(
            "warning",
            "This is a CMakeTest section definition, do not call this manually.")
        d.text(self.doc)


@dataclass
class MethodDocumentation(DocumentationType):
    """
    This is a special documentation type that holds
    information on a class's method or constructor.

    Its :method:`process` method requires a directive
    created by :class:`ClassDocumentation`.

    It translates the CMakePP method definition into
    a Sphinx :code:`py:method` directive, with a note
    if it is a macro.
    """
    parent_class: str
    """The class that this method is defined as a part of."""

    param_types: List[str]
    """The types of the parameters to the method"""

    params: List[str]
    """The parameter names."""

    is_constructor: bool
    """Whether this method is a constructor."""

    is_macro: bool = False
    """Whether the linked command is a macro or a function. If true, a note saying so is generated."""

    def process(self, writer: Directive):
        params_pretty = ', '.join(
            self.params) + ("[, ...]" if "args" in self.param_types else "")
        d = writer.directive(
            "py:method", f"{self.name}({params_pretty})")
        if self.is_macro:
            d.directive(
                "note",
                "This member is a macro and so does not introduce a new scope")
        # if doc.is_constructor:
        #     info = d.directive("admonition", "info")
        #     info.text("This member is a constructor.")
        d.text(self.doc)
        for i in range(len(self.param_types)):
            if i >= len(self.params):
                break
            if f":param {self.params[i]}:" not in self.doc:
                d.field(f"param {self.params[i]}", "")
            if f":type {self.params[i]}:" not in self.doc:
                d.field(f"type {self.params[i]}", self.param_types[i])


@dataclass
class AttributeDocumentation(DocumentationType):
    """
    This is a special documentation type that stores
    information on a class's attributes. Its :method:`process`
    method takes a directive created by :class:`ClassDocumentation`.

    It translates the CMakePP attribute definition into a Sphinx
    :code:`py:attribute` directive, with a :code:`value` option if
    it has a default value.
    """
    parent_class: str
    """The class that defines this attribute."""

    default_value: str
    """The default value of this attribute, if it has one."""

    def process(self, writer: Directive):
        d = writer.directive("py:attribute", f"{self.name}")
        if self.default_value is not None:
            d.option("value", self.default_value)

        d.text(self.doc)


@dataclass
class ClassDocumentation(DocumentationType):
    """
    This is a documentation type that represents a CMakePP
    class definition. It holds information on all the class's
    constructors, methods, and attributes via :class:`MethodDocumentation`
    and :class:`AttributeDocumentation`. It also contains string identifiers
    for its superclasses and inner classes.

    This class translates the associated CMakePP class definition into a
    Sphinx :code:`py:class` directive, then loops over all constructors,
    methods, and attributes and calls their :method:`process` method
    to add their information to the class directive.
    """

    superclasses: List[str]
    """A list of any superclasses this class has, empty if none"""

    # Type hint needs string because ClassDocumentation
    # not fully processed yet
    inner_classes: List['ClassDocumentation']
    """Any classes defined within this class."""

    constructors: List[MethodDocumentation]
    """A list of method documentation objects describing the constructors this class has."""

    members: List[MethodDocumentation]
    """A list of method documentation objects describing the class's methods."""

    attributes: List[AttributeDocumentation]
    """A list of attribute documentation objects describing the class's attributes."""

    def process(self, writer: RSTWriter):
        d = writer.directive("py:class", f"{self.name}")
        if len(self.superclasses) > 0:
            bases = "Bases: " + \
                    ", ".join(
                        f":class:`{superclass}`" for superclass in self.superclasses)
            d.text(bases + '\n')
        d.text(self.doc)

        if len(self.constructors) > 0:
            d.text("**Additional Constructors**")
            for member in self.constructors:
                member.process(d)

        if len(self.members) > 0:
            d.text("**Methods**")
            for member in self.members:
                member.process(d)

        if len(self.attributes) > 0:
            d.text("**Attributes**")
            for attribute in self.attributes:
                attribute.process(d)

        if len(self.inner_classes) > 0:
            d.text("**Inner classes**")
            d.bulleted_list(*[interpreted_text("class", clazz.name) for clazz in self.inner_classes])


@dataclass
class ModuleDocumentation(DocumentationType):
    """
    Represents documentation for an entire CMake module
    """

    def process(self, writer: RSTWriter):
        module = writer.directive("module", self.name)
        if self.doc is not None and len(self.doc) != 0:
            module.text(self.doc)
