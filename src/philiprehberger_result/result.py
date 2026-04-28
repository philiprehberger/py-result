from __future__ import annotations

from typing import TypeVar, Generic, Callable, Union, Awaitable, Iterable

T = TypeVar("T")
U = TypeVar("U")
E = TypeVar("E")
F = TypeVar("F")


class Ok(Generic[T, E]):
    __match_args__ = ("value",)
    __slots__ = ("_value",)

    def __init__(self, value: T) -> None:
        self._value = value

    @property
    def value(self) -> T:
        return self._value

    def is_ok(self) -> bool:
        return True

    def is_err(self) -> bool:
        return False

    def map(self, fn: Callable[[T], U]) -> Result[U, E]:
        return Ok(fn(self._value))

    def map_err(self, fn: Callable[[E], F]) -> Result[T, F]:
        return Ok(self._value)

    def flat_map(self, fn: Callable[[T], Result[U, E]]) -> Result[U, E]:
        return fn(self._value)

    def or_else(self, fn: Callable[[E], Result[T, F]]) -> Result[T, F]:
        return self  # type: ignore

    def to_dict(self) -> dict:
        return {"ok": self._value}

    def unwrap(self) -> T:
        return self._value

    def unwrap_or(self, default: T) -> T:
        return self._value

    def unwrap_err(self) -> E:
        raise ValueError("Called unwrap_err on Ok")

    def match(self, *, ok: Callable[[T], U], err: Callable[[E], U]) -> U:
        return ok(self._value)

    def with_context(self, msg: str) -> Result[T, E]:
        """Return self unchanged since this is an Ok value."""
        return self

    def __repr__(self) -> str:
        return f"Ok({self._value!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Ok):
            return self._value == other._value
        return NotImplemented

    def flatten(self) -> Result:
        """Flatten nested Results: Ok(Ok(v)) -> Ok(v), Ok(Err(e)) -> Err(e)."""
        if isinstance(self._value, (Ok, Err)):
            return self._value
        return self

    def transpose(self) -> Result:
        """Collapse a nested Result: Ok(Ok(v)) -> Ok(v), Ok(Err(e)) -> Err(e).

        Raises TypeError if the inner value is not a Result, since transpose
        only makes sense on nested Results.
        """
        if isinstance(self._value, (Ok, Err)):
            return self._value
        raise TypeError("Cannot transpose Ok[T] where T is not a Result")

    def __hash__(self) -> int:
        return hash(("Ok", self._value))


class Err(Generic[T, E]):
    __match_args__ = ("error",)
    __slots__ = ("_error",)

    def __init__(self, error: E) -> None:
        self._error = error

    @property
    def error(self) -> E:
        return self._error

    def is_ok(self) -> bool:
        return False

    def is_err(self) -> bool:
        return True

    def map(self, fn: Callable[[T], U]) -> Result[U, E]:
        return Err(self._error)

    def map_err(self, fn: Callable[[E], F]) -> Result[T, F]:
        return Err(fn(self._error))

    def flat_map(self, fn: Callable[[T], Result[U, E]]) -> Result[U, E]:
        return Err(self._error)

    def or_else(self, fn: Callable[[E], Result[T, F]]) -> Result[T, F]:
        return fn(self._error)

    def to_dict(self) -> dict:
        return {"err": self._error}

    def unwrap(self) -> T:
        if isinstance(self._error, BaseException):
            raise self._error
        raise ValueError(f"Called unwrap on Err: {self._error}")

    def unwrap_or(self, default: T) -> T:
        return default

    def unwrap_err(self) -> E:
        return self._error

    def match(self, *, ok: Callable[[T], U], err: Callable[[E], U]) -> U:
        return err(self._error)

    def with_context(self, msg: str) -> Result[T, str]:
        """Wrap the error value with additional context string."""
        return Err(f"{msg}: {self._error}")

    def __repr__(self) -> str:
        return f"Err({self._error!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Err):
            return self._error == other._error
        return NotImplemented

    def flatten(self) -> Result:
        """Flatten nested Results: Err(e) -> Err(e)."""
        return self

    def transpose(self) -> Result:
        """Collapse a nested Result: Err(e) -> Err(e)."""
        return self

    def __hash__(self) -> int:
        return hash(("Err", self._error))


Result = Union[Ok[T, E], Err[T, E]]


def ok(value: T) -> Ok[T, E]:
    return Ok(value)


def err(error: E) -> Err[T, E]:
    return Err(error)


def try_catch(fn: Callable[[], T]) -> Result[T, Exception]:
    try:
        return Ok(fn())
    except Exception as e:
        return Err(e)


async def try_catch_async(fn: Callable[[], Awaitable[T]]) -> Result[T, Exception]:
    try:
        return Ok(await fn())
    except Exception as e:
        return Err(e)


async def from_awaitable(awaitable: Awaitable[T]) -> Result[T, Exception]:
    try:
        return Ok(await awaitable)
    except Exception as e:
        return Err(e)


def all_ok(results: list[Result[T, E]]) -> Result[list[T], E]:
    values: list[T] = []
    for result in results:
        if result.is_err():
            return Err(result.unwrap_err())
        values.append(result.unwrap())
    return Ok(values)


def map_batch(results: list[Result[T, E]], fn: Callable[[T], U]) -> Result[list[U], E]:
    """Apply fn to all Ok values; short-circuit on first Err."""
    mapped: list[U] = []
    for result in results:
        if result.is_err():
            return Err(result.unwrap_err())
        mapped.append(fn(result.unwrap()))
    return Ok(mapped)


def combine(*results: Result) -> Result[tuple, object]:
    """Take multiple Results and return Ok(tuple of values) if all Ok, or the first Err."""
    values: list[object] = []
    for result in results:
        if result.is_err():
            return Err(result.unwrap_err())
        values.append(result.unwrap())
    return Ok(tuple(values))


def collect(iterable: Iterable[Result]) -> Result[list, object]:
    """Convert an iterable of Result objects into a Result containing a list of Ok values, or the first Err."""
    values: list[object] = []
    for result in iterable:
        if result.is_err():
            return Err(result.unwrap_err())
        values.append(result.unwrap())
    return Ok(values)


def transpose(result: Result) -> Result:
    """Collapse a nested Result: Ok(Ok(v)) -> Ok(v), Ok(Err(e)) -> Err(e), Err(e) -> Err(e)."""
    return result.transpose()
