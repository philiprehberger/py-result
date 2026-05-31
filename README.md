# philiprehberger-result

[![Tests](https://github.com/philiprehberger/py-result/actions/workflows/publish.yml/badge.svg)](https://github.com/philiprehberger/py-result/actions/workflows/publish.yml)
[![PyPI version](https://img.shields.io/pypi/v/philiprehberger-result.svg)](https://pypi.org/project/philiprehberger-result/)
[![Last updated](https://img.shields.io/github/last-commit/philiprehberger/py-result)](https://github.com/philiprehberger/py-result/commits/main)

Rust-inspired Result type for Python with pattern matching and type-safe error handling.

## Installation

```bash
pip install philiprehberger-result
```

## Usage

### Basic Result

```python
from philiprehberger_result import Ok, Err, Result

def divide(a: float, b: float) -> Result[float, str]:
    if b == 0:
        return Err("division by zero")
    return Ok(a / b)

result = divide(10, 2)
print(result.unwrap())  # 5.0

result = divide(10, 0)
print(result.unwrap_or(0.0))  # 0.0
```

### Pattern Matching (Python 3.10+)

```python
match divide(10, 3):
    case Ok(value):
        print(f"Result: {value}")
    case Err(error):
        print(f"Error: {error}")
```

### Chaining

```python
result = (
    Ok(10)
    .map(lambda x: x * 2)
    .flat_map(lambda x: Ok(x + 1) if x < 100 else Err("too large"))
)
```

### Fallback with or_else

```python
result = Err("not found").or_else(lambda e: Ok("default"))
# Ok("default")
```

### Serialization

```python
Ok(42).to_dict()    # {"ok": 42}
Err("x").to_dict()  # {"err": "x"}
```

### Try/Catch Wrapping

```python
from philiprehberger_result import try_catch

result = try_catch(lambda: int("not a number"))
# Err(ValueError("invalid literal..."))
```

### Async Support

```python
from philiprehberger_result import try_catch_async

result = await try_catch_async(fetch_data)
```

### Collecting Results

```python
from philiprehberger_result import all_ok

results = [Ok(1), Ok(2), Ok(3)]
combined = all_ok(results)  # Ok([1, 2, 3])

results = [Ok(1), Err("fail"), Ok(3)]
combined = all_ok(results)  # Err("fail")
```

### Batch Mapping

```python
from philiprehberger_result import map_batch

results = [Ok(1), Ok(2), Ok(3)]
mapped = map_batch(results, lambda x: x * 10)  # Ok([10, 20, 30])

results = [Ok(1), Err("fail"), Ok(3)]
mapped = map_batch(results, lambda x: x * 10)  # Err("fail")
```

### Flattening Nested Results

```python
nested = Ok(Ok(42))
flat = nested.flatten()  # Ok(42)

nested = Ok(Err("inner error"))
flat = nested.flatten()  # Err("inner error")

outer_err = Err("outer")
flat = outer_err.flatten()  # Err("outer")
```

### Transpose nested results

```python
from philiprehberger_result import transpose

transpose(Ok(Ok(5)))       # Ok(5)
transpose(Ok(Err("bad")))  # Err("bad")
transpose(Err("outer"))    # Err("outer")

# Method form:
Ok(Ok(5)).transpose()      # Ok(5)
Ok(Err("bad")).transpose() # Err("bad")
```

Unlike `flatten()`, `transpose()` collapses both inner branches and raises
`TypeError` if the inner value is not itself a `Result`.

### Combining Multiple Results

```python
from philiprehberger_result import combine

result = combine(Ok(1), Ok("hello"), Ok(True))
# Ok((1, "hello", True))

result = combine(Ok(1), Err("fail"), Ok(3))
# Err("fail")
```

### Collecting Results from Iterables

```python
from philiprehberger_result import collect

results = [Ok(1), Ok(2), Ok(3)]
collected = collect(results)  # Ok([1, 2, 3])

results = [Ok(1), Err("fail"), Ok(3)]
collected = collect(results)  # Err("fail")
```

### Adding Error Context

```python
result = Err("not found").with_context("loading config")
# Err("loading config: not found")

ok_result = Ok(42).with_context("ignored for Ok")
# Ok(42)
```

### Partitioning

```python
from philiprehberger_result import Ok, Err, partition

oks, errs = partition([Ok(1), Err("a"), Ok(2), Err("b"), Ok(3)])
# oks == [1, 2, 3]
# errs == ["a", "b"]
```

Unlike `collect()`, `partition()` does not short-circuit on the first `Err` —
it walks the entire iterable and returns both lists.

### Side-effect taps

```python
from philiprehberger_result import Ok, Err

Ok(5).tap(lambda v: print(f"got {v}"))
# prints "got 5", returns Ok(5)

Err("boom").tap_err(lambda e: print(f"error: {e}"))
# prints "error: boom", returns Err("boom")

# Mismatched variants are no-ops:
Err("boom").tap(lambda v: print(v))      # does nothing, returns Err("boom")
Ok(5).tap_err(lambda e: print(e))        # does nothing, returns Ok(5)
```

## API

| Function / Class | Description |
|---|---|
| `Ok(value)` | Success variant — wraps a value |
| `Err(error)` | Error variant — wraps an error |
| `.is_ok()` / `.is_err()` | Type check |
| `.unwrap()` | Get value or raise |
| `.unwrap_or(default)` | Get value or return default |
| `.unwrap_err()` | Get error or raise |
| `.map(fn)` | Transform Ok value |
| `.map_err(fn)` | Transform Err value |
| `.flat_map(fn)` | Chain Result-returning functions |
| `.or_else(fn)` | Fallback on Err, pass-through on Ok |
| `.flatten()` | Flatten nested Results: `Ok(Ok(v))` -> `Ok(v)` |
| `.transpose()` / `transpose(result)` | Collapse nested Result: `Ok(Ok(v))` -> `Ok(v)`, `Ok(Err(e))` -> `Err(e)`, `Err(e)` -> `Err(e)` |
| `.match(ok=fn, err=fn)` | Pattern dispatch |
| `.to_dict()` | Serialize to `{"ok": v}` or `{"err": e}` |
| `ok(value)` / `err(error)` | Shorthand constructors |
| `try_catch(fn)` | Wrap callable in Result |
| `try_catch_async(fn)` | Async version |
| `from_awaitable(aw)` | Wrap awaitable in Result |
| `all_ok(results)` | Collect list of Results into Result of list |
| `map_batch(results, fn)` | Apply fn to all Ok values; short-circuit on first Err |
| `combine(*results)` | Merge multiple Results into Ok(tuple) or first Err |
| `collect(iterable)` | Convert iterable of Results into Result of list or first Err |
| `partition(results)` | Split iterable of Results into `(oks, errs)` lists without short-circuiting |
| `.with_context(msg)` | Wrap Err with context string; pass-through on Ok |
| `Ok.tap(fn)` / `Err.tap(fn)` | Call `fn(value)` on Ok for side effects; no-op on Err; returns self |
| `Ok.tap_err(fn)` / `Err.tap_err(fn)` | Call `fn(error)` on Err for side effects; no-op on Ok; returns self |

## Development

```bash
pip install -e .
python -m pytest tests/ -v
```

## Support

If you find this project useful:

⭐ [Star the repo](https://github.com/philiprehberger/py-result)

🐛 [Report issues](https://github.com/philiprehberger/py-result/issues?q=is%3Aissue+is%3Aopen+label%3Abug)

💡 [Suggest features](https://github.com/philiprehberger/py-result/issues?q=is%3Aissue+is%3Aopen+label%3Aenhancement)

❤️ [Sponsor development](https://github.com/sponsors/philiprehberger)

🌐 [All Open Source Projects](https://philiprehberger.com/open-source-packages)

💻 [GitHub Profile](https://github.com/philiprehberger)

🔗 [LinkedIn Profile](https://www.linkedin.com/in/philiprehberger)

## License

[MIT](LICENSE)
