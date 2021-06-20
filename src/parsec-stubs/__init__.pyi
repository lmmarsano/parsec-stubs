import collections as C
import collections.abc as CA
import re
import typing as T

_U = T.TypeVar("_U")
_V = T.TypeVar("_V")
_W = T.TypeVar("_W")
_VS = T.TypeVar("_VS", bound=CA.Sequence)
_LocInfo = tuple[int, int]

class ParseError(RuntimeError):
    expect: str
    text: CA.Sequence
    index: int
    def __init__(self, expected: str, text: CA.Sequence, index: int) -> None: ...
    @staticmethod
    def loc_info(text: CA.Sequence, index: int) -> _LocInfo: ...
    def loc(self) -> str: ...
    def __str__(self) -> str: ...

class Value(C.namedtuple("Value", "status index value expected"), T.Generic[_U]):
    @staticmethod
    def success(index: int, actual: _U) -> Value[_U]: ...
    @staticmethod
    def failure(index: int, expected: str) -> Value[_U]: ...
    def aggregate(
        self: Value[CA.Sequence[_V]], other: T.Optional[Value[CA.Sequence[_V]]] = ...
    ) -> Value[CA.Sequence[_V]]: ...
    @staticmethod
    def combinate(values: CA.Iterable[Value[_V]]) -> Value[tuple[_V, ...]]: ...
    def __str__(self) -> str: ...

class Parser(T.Generic[_U]):
    def __init__(self, fn: CA.Callable[[str, int], Value[_U]]) -> None: ...
    def __call__(self, text: CA.Sequence, index: int) -> Value[_U]: ...
    def parse(self, text: CA.Sequence) -> _U: ...
    def parse_partial(self, text: CA.Sequence) -> tuple[_U, str]: ...
    def parse_strict(self, text: CA.Sequence) -> _U: ...
    def bind(self, fn: CA.Callable[[_U], Parser[_V]]) -> Parser[_V]: ...
    def compose(self, other: Parser[_V]) -> Parser[_V]: ...
    def joint(self, *parsers: Parser[_U]) -> Parser[tuple[_U, ...]]: ...
    def choice(self, other: Parser[_V]) -> Parser[_U | _V]: ...
    def try_choice(self, other: Parser[_V]) -> Parser[_U | _V]: ...
    def skip(self, other: Parser) -> Parser[_U]: ...
    def ends_with(self, other: Parser) -> Parser[_U]: ...
    def parsecmap(self, fn: CA.Callable[[_U], _V]) -> Parser[_V]: ...
    def parsecapp(
        self: Parser[CA.Callable[[_V], _W]], other: Parser[_V]
    ) -> Parser[_W]: ...
    def result(self, res: _V) -> Parser[_V]: ...
    def mark(self) -> Parser[tuple[_LocInfo, _U, _LocInfo]]: ...
    def desc(self, description: str) -> Parser[_U]: ...
    def __or__(self, other: Parser[_V]) -> Parser[_U | _V]: ...
    def __xor__(self, other: Parser[_V]) -> Parser[_U | _V]: ...
    def __add__(self, other: Parser[_V]) -> Parser[tuple[_U, _V]]: ...
    def __rshift__(self, other: Parser[_V]) -> Parser[_V]: ...
    def __irshift__(self, other: CA.Callable[[_U], Parser[_V]]) -> Parser[_V]: ...
    def __lshift__(self, other: Parser) -> Parser[_U]: ...
    def __lt__(self, other: Parser) -> Parser[_U]: ...

def parse(p: Parser[_V], text: CA.Sequence, index: int) -> _V: ...
def bind(p: Parser[_U], fn: CA.Callable[[_U], Parser[_V]]) -> Parser[_V]: ...
def compose(pa: Parser, pb: Parser[_V]) -> Parser[_V]: ...
def joint(*parsers: Parser[_U]) -> Parser[tuple[_U, ...]]: ...
def choice(pa: Parser[_U], pb: Parser[_V]) -> Parser[_U | _V]: ...
def try_choice(pa: Parser[_U], pb: Parser[_V]) -> Parser[_U | _V]: ...
def skip(pa: Parser[_U], pb: Parser) -> Parser[_U]: ...
def ends_with(pa: Parser[_U], pb: Parser) -> Parser[_U]: ...
def parsecmap(p: Parser[_U], fn: CA.Callable[[_U], _V]) -> Parser[_V]: ...
def parsecapp(p: Parser[CA.Callable[[_U], _V]], other: Parser[_U]) -> Parser[_V]: ...
def result(p: Parser, res: _U) -> Parser[_U]: ...
def mark(p: Parser[_U]) -> Parser[tuple[_LocInfo, _U, _LocInfo]]: ...
def desc(p: Parser[_U], description: str) -> Parser[_U]: ...
@T.overload
def generate(
    fn: str,
) -> CA.Callable[
    [CA.Callable[[], CA.Generator[Parser[_U], _U, Parser[_V] | _V]]], Parser[_V]
]: ...
@T.overload
def generate(
    fn: CA.Callable[[], CA.Generator[Parser[_U], _U, Parser[_V] | _V]]
) -> Parser[_V]: ...
def times(
    p: Parser[_U], mint: int, maxt: T.Optional[float] = ...
) -> Parser[list[_U]]: ...
def count(p: Parser[_U], n: int) -> Parser[list[_U]]: ...
def optional(
    p: Parser[_U], default_value: T.Optional[_V] = ...
) -> Parser[_U | _V | None]: ...
def many(p: Parser[_U]) -> Parser[list[_U]]: ...
def many1(p: Parser[_U]) -> Parser[list[_U]]: ...
def separated(
    p: Parser[_U],
    sep: Parser,
    mint: int,
    maxt: T.Optional[int] = ...,
    end: T.Optional[bool] = ...,
) -> Parser[list[_U]]: ...
def sepBy(p: Parser[_U], sep: Parser) -> Parser[list[_U]]: ...
def sepBy1(p: Parser[_U], sep: Parser) -> Parser[list[_U]]: ...
def endBy(p: Parser[_U], sep: Parser) -> Parser[list[_U]]: ...
def endBy1(p: Parser[_U], sep: Parser) -> Parser[list[_U]]: ...
def sepEndBy(p: Parser[_U], sep: Parser) -> Parser[list[_U]]: ...
def sepEndBy1(p: Parser[_U], sep: Parser) -> Parser[list[_U]]: ...
def any() -> Parser: ...
def one_of(s: CA.Container[_U]) -> Parser[_U]: ...
def none_of(s: CA.Container[_U]) -> Parser[_U]: ...
def space() -> Parser[str]: ...
def spaces() -> Parser[list[str]]: ...
def letter() -> Parser[str]: ...
def digit() -> Parser[str]: ...
def eof() -> Parser[None]: ...
def string(s: _VS) -> Parser[_VS]: ...
def regex(exp: str | re.Pattern, flags: re.RegexFlag = ...) -> Parser[str]: ...
def fail_with(message: str) -> Parser: ...
def exclude(p: Parser[_U], exclude: Parser) -> Parser[_U]: ...
def lookahead(p: Parser[_U]) -> Parser[_U]: ...
def unit(p: Parser[_U]) -> Parser[_U]: ...
