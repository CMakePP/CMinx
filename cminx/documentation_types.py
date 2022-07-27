from collections import namedtuple
from enum import Enum

AttributeDocumentation = namedtuple(
    'AttributeDocumentation', 'parent_class name default_value doc')
FunctionDocumentation = namedtuple(
    'FunctionDocumentation', 'function params doc')
MacroDocumentation = namedtuple("MacroDocumentation", "macro params doc")
VariableDocumentation = namedtuple(
    'VariableDocumentation', 'varname type value doc')
GenericCommandDocumentation = namedtuple(
    'GenericCommandDocumentation', 'name params doc')
ClassDocumentation = namedtuple(
    'ClassDocumentation', 'name superclasses inner_classes constructors members attributes doc')


class TestDocumentation:
    def __init__(self, name: str, expect_fail: bool, doc: str) -> None:
        self.name = name
        self.expect_fail = expect_fail
        self.doc = doc
        self.params = []
        self.is_macro = False


class SectionDocumentation:
    def __init__(self, name: str, expect_fail: bool, doc: str) -> None:
        self.name = name
        self.expect_fail = expect_fail
        self.doc = doc
        self.params = []
        self.is_macro = False


class MethodDocumentation:
    def __init__(self, parent_class, name, param_types, params, is_constructor, doc) -> None:
        self.parent_class = parent_class
        self.name = name
        self.param_types = param_types
        self.params = params
        self.is_constructor = is_constructor
        self.doc = doc
        self.is_macro = False


DOC_TYPES = (FunctionDocumentation, MacroDocumentation, VariableDocumentation,
             TestDocumentation, SectionDocumentation, GenericCommandDocumentation,
             ClassDocumentation, AttributeDocumentation, MethodDocumentation)
VarType = Enum("VarType", "String List Unset")
