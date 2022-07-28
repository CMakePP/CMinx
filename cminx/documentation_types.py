from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum

from .rstwriter import RSTWriter, Directive


class VarType(Enum):
    STRING = 1
    LIST = 2
    UNSET = 3


class DocumentationType(ABC):
    """
    This is the base class for all documentation types. It defines a single
    abstract process() method that is used to write the documentation RST
    to a given :class:`RSTWriter`.
    """

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
class FunctionDocumentation(DocumentationType):
    """
    This class serves as the representation of a documented
    CMake function definition. It converts the function definition
    directly to a Sphinx :code:`function` directive.
    """

    function: str
    params: list[str]
    doc: str

    def process(self, writer: RSTWriter):
        d = writer.directive(
            "function", f"{self.function}({' '.join(self.params)})")
        d.text(self.doc)


@dataclass
class MacroDocumentation(DocumentationType):
    """
    This class serves as the representation of a documented
    CMake macro definition. It converts the macro definition
    directly to a Sphinx :code:`function` directive and adds a
    :code:`warning` directive specifying that it is a macro.
    """
    macro: str
    params: list[str]
    doc: str

    def process(self, writer: RSTWriter):
        d = writer.directive(
            "function", f"{self.macro}({' '.join(self.params)})")
        d.directive(
            "warning",
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

    varname: str
    type: VarType
    value: str
    doc: str

    def process(self, writer: RSTWriter):
        d = writer.directive("data", f"{self.varname}")
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
class GenericCommandDocumentation(DocumentationType):
    """
    This class represents any documented command that does
    not fit into any of the other documentation types.

    All this class does is translate the documented
    command into a Sphinx :code:`function` directive with
    a warning that it is a command invocation and not
    a definition.
    """
    name: str
    params: list[str]
    doc: str

    def process(self, writer: RSTWriter):
        d = writer.directive(
            "function", f"{self.name}({' '.join(self.params)})")
        d.directive(
            "warning",
            "This is a generic command invocation. It is not a function or macro definition.")
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
    name: str
    expect_fail: bool
    doc: str
    params: list[str] = field(default_factory=lambda: [])
    is_macro: bool = False

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
    name: str
    param_types: list[str]
    params: list[str]
    is_constructor: bool
    doc: str
    is_macro: bool = False

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
    name: str
    default_value: str
    doc: str

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
    name: str
    superclasses: list[str]
    inner_classes: list
    constructors: list[MethodDocumentation]
    members: list[MethodDocumentation]
    attributes: list[AttributeDocumentation]
    doc: str

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
