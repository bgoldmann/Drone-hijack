# Test Suite

This directory contains unit, integration, and end-to-end tests for the new features.

## Test Structure

- `test_progress_api.py`: Tests for progress tracking API endpoints
- `test_config_api.py`: Tests for configuration API endpoints
- `test_exploits_api.py`: Tests for exploits API endpoints
- `test_export_api.py`: Tests for export API endpoints

## Running Tests

### Install Dependencies

```bash
pip install pytest pytest-flask
```

### Run All Tests

```bash
pytest tests/
```

### Run Specific Test File

```bash
pytest tests/test_progress_api.py
```

### Run with Coverage

```bash
pytest --cov=. --cov-report=html tests/
```

## Test Coverage

Current test coverage includes:

- [x] Progress tracking API endpoints
- [x] Configuration API endpoints
- [x] Exploits API endpoints
- [x] Export API endpoints
- [ ] Integration tests for attack chains
- [ ] End-to-end tests for complete workflows

## Notes

- Tests use in-memory SQLite database for isolation
- Mock filesystem operations where needed
- Tests should be run in isolated environment
