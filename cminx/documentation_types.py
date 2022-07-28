from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum

from rstwriter import RSTWriter


class VarType(Enum):
    STRING = 1
    LIST = 2
    UNSET = 3


class Documentation(ABC):
    """
    This is the base class for all documentation types. It defines a single
    abstract process() method that is used to write the documentation RST
    to a given RSTWriter.
    """

    @abstractmethod
    def process(self, writer: RSTWriter):
        pass


@dataclass
class FunctionDocumentation(Documentation):
    function: str
    params: list[str]
    doc: str

    def process(self, writer: RSTWriter):
        d = writer.directive(
            "function", f"{self.function}({' '.join(self.params)})")
        d.text(self.doc)


@dataclass
class MacroDocumentation(Documentation):
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
class VariableDocumentation(Documentation):
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
class GenericCommandDocumentation(Documentation):
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
class TestDocumentation(Documentation):
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

    def process(self, writer: RSTWriter):
        d = writer.directive(
            "function",
            f"{self.name}({'EXPECTFAIL' if self.expect_fail else ''})")
        d.directive(
            "warning",
            "This is a CMakeTest section definition, do not call this manually.")
        d.text(self.doc)


@dataclass
class MethodDocumentation(Documentation):
    parent_class: str
    name: str
    param_types: list[str]
    params: list[str]
    is_constructor: bool
    doc: str
    is_macro: bool = False

    def process(self, writer: RSTWriter):
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
class AttributeDocumentation(Documentation):
    parent_class: str
    name: str
    default_value: str
    doc: str

    def process(self, writer: RSTWriter):
        d = writer.directive("py:attribute", f"{self.name}")
        if self.default_value is not None:
            d.option("value", self.default_value)

        d.text(self.doc)


@dataclass
class ClassDocumentation(Documentation):
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
