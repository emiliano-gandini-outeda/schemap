"""Tests for SchemaConfig."""

import pytest
from schemap.base import AutoBase
from schemap.config import SchemaConfig
from sqlalchemy.orm import Mapped, mapped_column

class User(AutoBase):
    __tablename__ = "config_users"
    __schema_config__ = SchemaConfig(
        exclude_public=["email"],
        exclude_create=["internal_id"],
    )
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    internal_id: Mapped[int] = mapped_column()

def test_exclude_from_public():
    """Test that email is excluded from PublicSchema."""
    assert "email" not in User.PublicSchema.model_fields
    assert "name" in User.PublicSchema.model_fields

def test_exclude_from_create():
    """Test that internal_id is excluded from CreateSchema."""
    assert "internal_id" not in User.CreateSchema.model_fields
    assert "name" in User.CreateSchema.model_fields

def test_default_schema_untouched():
    """Test that default Schema still has all fields."""
    assert "email" in User.Schema.model_fields
    assert "internal_id" in User.Schema.model_fields