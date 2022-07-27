from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum

from rstwriter import RSTWriter

VarType = Enum("VarType", "String List Unset")


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
        pass


@dataclass
class MacroDocumentation(Documentation):
    macro: str
    params: list[str]
    doc: str

    def process(self, writer: RSTWriter):
        pass


@dataclass
class VariableDocumentation(Documentation):
    varname: str
    type: VarType
    value: str
    doc: str

    def process(self, writer: RSTWriter):
        pass


@dataclass
class GenericCommandDocumentation(Documentation):
    name: str
    params: list[str]
    doc: str

    def process(self, writer: RSTWriter):
        pass


@dataclass
class TestDocumentation(Documentation):
    name: str
    expect_fail: bool
    doc: str
    params: list[str] = field(default_factory=lambda: [])
    is_macro: bool = False

    def process(self, writer: RSTWriter):
        pass


@dataclass
class SectionDocumentation(TestDocumentation):

    def process(self, writer: RSTWriter):
        pass


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
        pass


@dataclass
class AttributeDocumentation(Documentation):
    parent_class: str
    name: str
    default_value: str
    doc: str

    def process(self, writer: RSTWriter):
        pass


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
        pass
