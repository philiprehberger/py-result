# philiprehberger-result

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

## License

MIT
