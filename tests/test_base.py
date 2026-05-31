"""Tests for AutoBase and SchemaMixin."""

import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from schemap.base import AutoBase
from sqlalchemy.orm import Mapped, mapped_column


class User(AutoBase):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)


def test_auto_schemas_exist():
    """Test that schemas are auto-generated as class attributes."""
    assert hasattr(User, "Schema")
    assert hasattr(User, "CreateSchema")
    assert hasattr(User, "UpdateSchema")
    assert hasattr(User, "PublicSchema")


def test_from_schema_creates_instance():
    """Test creating ORM instance from Pydantic schema."""
    data = User.CreateSchema(username="alice", email="alice@example.com")
    user = User.from_schema(data)
    
    assert user.username == "alice"
    assert user.email == "alice@example.com"
    assert user.id is None  # Not set because excluded from CreateSchema


def test_to_schema_converts_instance():
    """Test converting ORM instance to Pydantic schema."""
    user = User(id=1, username="bob", email="bob@example.com")
    schema = user.to_schema()
    
    assert schema.username == "bob"
    assert schema.email == "bob@example.com"
    assert schema.id == 1


def test_round_trip():
    """Test ORM -> Schema -> ORM round trip."""
    original = User(id=5, username="charlie", email="charlie@example.com")
    schema = original.to_schema()
    rehydrated = User.from_schema(schema)
    
    assert rehydrated.username == original.username
    assert rehydrated.email == original.email
    assert rehydrated.id == original.id