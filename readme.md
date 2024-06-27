# Backend Frameworks

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)

A series of framework classes to facilitate [database management](src/db_framework/), [user account creation](src/user_framework/) and [payment processing](src/payment_framework/).

## Setup .venv

Ensure virtualenv command is available and run:

```
virtualenv -p=3.11 .venv
```

MAC:
```
source .venv/bin/activate
```

WIN:
```
.\venv\Scripts\activate
```

## Requirements:

```
pip install -r requirements.txt
```

- boto3: AWS Python Client
- moto: Mock boto3 for offline testing
- pytest: For testing
- pytest-watcher: Watch for file updates

*plus sub dependencies*

## Testing:

Pytest is used for testing by running

```
pytest
```

Or with logging enabled

```
pytest -o log_cli=true

```

Watch for file changes and re-run tests with pytest-watcher

```
ptw .
```

Use `breakpoint()` to step through code and run

```
pytest -s
```







