"""Tests for type resolution."""

import pytest
from datetime import datetime, date
from sqlalchemy import Integer, String, Boolean, DateTime, Date, Float, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Column

from schemap.types import extract_python_type, extract_column_metadata


def test_simple_type_mapping():
    """Test that basic SQLAlchemy types map to correct Python types."""
    assert extract_python_type(Integer()) == (int, False)
    assert extract_python_type(String()) == (str, False)
    assert extract_python_type(Boolean()) == (bool, False)
    assert extract_python_type(Float()) == (float, False)
    assert extract_python_type(DateTime()) == (datetime, False)
    assert extract_python_type(Date()) == (date, False)
    assert extract_python_type(Text()) == (str, False)


def test_column_metadata_basics():
    """Test extraction of column properties."""
    
    col = Column("id", Integer, primary_key=True, nullable=False)
    metadata = extract_column_metadata(col)
    
    assert metadata["python_type"] == int
    assert metadata["is_optional"] is False
    assert metadata["primary_key"] is True


def test_string_length():
    """Test that String(100) captures max_length."""
    col = Column("name", String(100), nullable=False)
    metadata = extract_column_metadata(col)
    
    assert metadata["max_length"] == 100


def test_nullable_column():
    """Test that nullable=True sets is_optional=True."""
    col = Column("bio", Text, nullable=True)
    metadata = extract_column_metadata(col)
    
    assert metadata["is_optional"] is True