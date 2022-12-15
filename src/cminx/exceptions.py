import dataclasses


@dataclasses.dataclass
class CMakeSyntaxException(Exception):
    msg: str
    line: int
