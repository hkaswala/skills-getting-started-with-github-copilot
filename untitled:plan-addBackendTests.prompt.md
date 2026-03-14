# Plan: Add Backend FastAPI Tests in Separate tests Directory

## Objective
Add backend FastAPI tests for the Mergington High School API in a separate `tests/` directory. Keep tests isolated from mutable in-memory state and ensure they run from repo root using pytest.

## Structure
- Create `tests/` directory at project root.
- Add test file(s), e.g. `tests/test_app_endpoints.py`.

## Implementation Steps
1. Create `tests/` directory.
2. Create tests around the existing API endpoints using FastAPI `TestClient`:
   - `GET /activities`
   - `POST /activities/{activity_name}/signup`
   - `DELETE /activities/{activity_name}/signup`
3. Add fixture to restore in-memory `activities` state after each test (deep copy restore).
4. Write test cases for happy and error paths:
   - GET returns 200 and expected activity fields
   - POST sign-up success
   - POST non-existent activity 404
   - POST duplicate signup 400
   - DELETE remove success
   - DELETE missing activity 404
   - DELETE participant not found 404
5. Run `pytest -q` to verify all tests pass.

## Verification
- Ensure tests run and pass with `pytest -q`.
- Confirm endpoints still work in production.

## Improvements
- Add a `tests/conftest.py` fixture file for shared fixtures and set-up/teardown.
- Add API contract tests and negative scenarios for invalid query/params.
- Add `pytest-cov` and run coverage reports with `pytest --cov=src --cov-report=term`.
- Add a GitHub Actions workflow to run `pytest` on push and pull request.

