# philiprehberger-result

[![Tests](https://github.com/philiprehberger/py-result/actions/workflows/publish.yml/badge.svg)](https://github.com/philiprehberger/py-result/actions/workflows/publish.yml)
[![PyPI version](https://img.shields.io/pypi/v/philiprehberger-result.svg)](https://pypi.org/project/philiprehberger-result/)
[![License](https://img.shields.io/github/license/philiprehberger/py-result)](LICENSE)
[![Sponsor](https://img.shields.io/badge/sponsor-GitHub%20Sponsors-ec6cb9)](https://github.com/sponsors/philiprehberger)

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

## API Reference

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
| `.match(ok=fn, err=fn)` | Pattern dispatch |
| `.to_dict()` | Serialize to `{"ok": v}` or `{"err": e}` |
| `ok(value)` / `err(error)` | Shorthand constructors |
| `try_catch(fn)` | Wrap callable in Result |
| `try_catch_async(fn)` | Async version |
| `from_awaitable(aw)` | Wrap awaitable in Result |
| `all_ok(results)` | Collect list of Results into Result of list |


## Development

```bash
pip install -e .
python -m pytest tests/ -v
```

## License

MIT
