"""Verifies that the configured PostgreSQL connection actually works.

Requires a reachable PostgreSQL instance matching the environment
configuration (see .env.example). Skipped automatically if the database
is unreachable, so the rest of the test suite still runs in environments
without a database.
"""

import pytest
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from app.db.session import engine


def test_postgresql_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1")).scalar_one()
    except OperationalError as exc:
        pytest.skip(f"PostgreSQL is not reachable: {exc}")

    assert result == 1
