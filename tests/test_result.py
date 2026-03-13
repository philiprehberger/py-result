from __future__ import annotations

import asyncio

import pytest

from philiprehberger_result import Ok, Err, ok, err, try_catch, try_catch_async, from_awaitable, all_ok


# --- Ok basics ---

def test_ok_is_ok():
    assert Ok(1).is_ok() is True

def test_ok_is_err():
    assert Ok(1).is_err() is False

def test_ok_value():
    assert Ok(42).value == 42

def test_ok_unwrap():
    assert Ok("hello").unwrap() == "hello"

def test_ok_unwrap_or():
    assert Ok(10).unwrap_or(99) == 10


# --- Err basics ---

def test_err_is_ok():
    assert Err("fail").is_ok() is False

def test_err_is_err():
    assert Err("fail").is_err() is True

def test_err_error():
    assert Err("oops").error == "oops"

def test_err_unwrap_raises():
    with pytest.raises(ValueError):
        Err("not an exception").unwrap()

def test_err_unwrap_or():
    assert Err("fail").unwrap_or(42) == 42

def test_err_unwrap_err():
    assert Err("x").unwrap_err() == "x"


# --- Err.unwrap with exception ---

def test_err_unwrap_reraises_exception():
    original = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        Err(original).unwrap()


# --- Err.unwrap with non-exception ---

def test_err_unwrap_non_exception_raises_value_error():
    with pytest.raises(ValueError, match="Called unwrap on Err"):
        Err("just a string").unwrap()


# --- map ---

def test_ok_map():
    assert Ok(5).map(lambda x: x * 2) == Ok(10)

def test_err_map():
    assert Err("fail").map(lambda x: x * 2) == Err("fail")


# --- map_err ---

def test_ok_map_err():
    assert Ok(5).map_err(lambda e: e.upper()) == Ok(5)

def test_err_map_err():
    assert Err("fail").map_err(lambda e: e.upper()) == Err("FAIL")


# --- flat_map ---

def test_ok_flat_map():
    assert Ok(5).flat_map(lambda x: Ok(x + 1)) == Ok(6)

def test_err_flat_map():
    assert Err("fail").flat_map(lambda x: Ok(x + 1)) == Err("fail")


# --- or_else ---

def test_ok_or_else():
    result = Ok(5).or_else(lambda e: Ok(0))
    assert result == Ok(5)

def test_err_or_else():
    result = Err("fail").or_else(lambda e: Ok(len(e)))
    assert result == Ok(4)


# --- match ---

def test_ok_match():
    result = Ok(10).match(ok=lambda v: v * 2, err=lambda e: -1)
    assert result == 20

def test_err_match():
    result = Err("bad").match(ok=lambda v: v * 2, err=lambda e: e.upper())
    assert result == "BAD"


# --- to_dict ---

def test_ok_to_dict():
    assert Ok(42).to_dict() == {"ok": 42}

def test_err_to_dict():
    assert Err("fail").to_dict() == {"err": "fail"}


# --- Pattern matching ---

def test_pattern_match_ok():
    match Ok(99):
        case Ok(value):
            assert value == 99
        case _:
            pytest.fail("Should match Ok")

def test_pattern_match_err():
    match Err("x"):
        case Err(error):
            assert error == "x"
        case _:
            pytest.fail("Should match Err")


# --- Equality ---

def test_ok_equality():
    assert Ok(1) == Ok(1)
    assert Ok(1) != Ok(2)

def test_err_equality():
    assert Err("a") == Err("a")
    assert Err("a") != Err("b")


# --- Hash ---

def test_ok_hashable():
    assert hash(Ok(1)) == hash(Ok(1))
    s = {Ok(1), Ok(1), Ok(2)}
    assert len(s) == 2

def test_err_hashable():
    assert hash(Err("a")) == hash(Err("a"))


# --- repr ---

def test_ok_repr():
    assert repr(Ok(1)) == "Ok(1)"

def test_err_repr():
    assert repr(Err("x")) == "Err('x')"


# --- Helper functions ---

def test_ok_helper():
    assert ok(1) == Ok(1)

def test_err_helper():
    assert err("x") == Err("x")


# --- try_catch ---

def test_try_catch_success():
    result = try_catch(lambda: 42)
    assert result == Ok(42)

def test_try_catch_failure():
    result = try_catch(lambda: (_ for _ in ()).throw(ValueError("bad")))
    assert result.is_err()
    assert isinstance(result.unwrap_err(), ValueError)


# --- try_catch_async ---

def test_try_catch_async_success():
    async def fn():
        return 42
    result = asyncio.run(try_catch_async(fn))
    assert result == Ok(42)

def test_try_catch_async_failure():
    async def fn():
        raise ValueError("async bad")
    result = asyncio.run(try_catch_async(fn))
    assert result.is_err()


# --- from_awaitable ---

def test_from_awaitable_success():
    async def main():
        async def coro():
            return 99
        return await from_awaitable(coro())
    result = asyncio.run(main())
    assert result == Ok(99)


# --- all_ok ---

def test_all_ok_success():
    result = all_ok([Ok(1), Ok(2), Ok(3)])
    assert result == Ok([1, 2, 3])

def test_all_ok_with_err():
    result = all_ok([Ok(1), Err("fail"), Ok(3)])
    assert result == Err("fail")
