from abc import ABC, abstractmethod
from dataclasses import dataclass
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


class TestDocumentation(Documentation):
    def __init__(self, name: str, expect_fail: bool, doc: str) -> None:
        self.name = name
        self.expect_fail = expect_fail
        self.doc = doc
        self.params = []
        self.is_macro = False

    def process(self, writer: RSTWriter):
        pass


class SectionDocumentation(Documentation):
    def __init__(self, name: str, expect_fail: bool, doc: str) -> None:
        self.name = name
        self.expect_fail = expect_fail
        self.doc = doc
        self.params = []
        self.is_macro = False

    def process(self, writer: RSTWriter):
        pass


class MethodDocumentation(Documentation):
    def __init__(self, parent_class, name, param_types, params, is_constructor, doc) -> None:
        self.parent_class = parent_class
        self.name = name
        self.param_types = param_types
        self.params = params
        self.is_constructor = is_constructor
        self.doc = doc
        self.is_macro = False

    def process(self, writer: RSTWriter):
        pass


@dataclass
class AttributeDocumentation(Documentation):
    parent_class: object
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


DOC_TYPES = (FunctionDocumentation, MacroDocumentation, VariableDocumentation,
             TestDocumentation, SectionDocumentation, GenericCommandDocumentation,
             ClassDocumentation, AttributeDocumentation, MethodDocumentation)

