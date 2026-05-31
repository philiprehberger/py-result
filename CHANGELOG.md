# Changelog

## 0.6.0 (2026-05-30)

- Add `partition()` splitting an iterable of Results into `(oks, errs)` lists without short-circuiting
- Add `Result.tap()` and `Result.tap_err()` for side-effect callbacks that leave the value unchanged

## 0.5.0 (2026-04-27)

- Add `transpose()` method on `Ok`/`Err` and top-level `transpose()` function for collapsing nested Result types

## 0.4.1 (2026-03-31)

- Standardize README to 3-badge format with emoji Support section
- Update CI checkout action to v5 for Node.js 24 compatibility

## 0.4.0 (2026-03-28)

- Add `combine()` function to merge multiple Results into Ok(tuple) or first Err
- Add `with_context()` method for wrapping errors with context strings
- Add `collect()` function to convert iterables of Results into a single Result
- Bring package into full compliance with guides

## 0.3.0 (2026-03-27)

- Add `map_batch()` function for batch mapping over a list of Results
- Add `flatten()` method on Ok and Err for flattening nested Results
- Add 8 badges, Support section, and compliance fixes to README
- Add `[tool.pytest.ini_options]` and `[tool.mypy]` to pyproject.toml
- Add `.github/` issue templates, PR template, and Dependabot config

## 0.2.3 (2026-03-22)

- Add Development section to README
- Add wheel build target to pyproject.toml

## 0.2.0 (2026-03-18)

- Add `or_else()` method to Ok and Err for fallback chaining
- Add `to_dict()` method for serialization
- Fix `all_ok` type handling
- Add comprehensive test suite (~30 tests)
- Add API reference table to README

## 0.1.1 (2026-03-12)

- Add project URLs to pyproject.toml

## 0.1.0 (2026-03-10)
- Initial release
