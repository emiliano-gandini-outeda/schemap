from __future__ import annotations

from typing import Callable, TypeVar, overload

from .builder import build_schema
from .config import SchemaConfig
from .methods import _from_schema, _to_schema

T = TypeVar("T")


def _apply_auto_schema(cls: type, config: SchemaConfig | None) -> type:
    cfg = config or SchemaConfig()
    cls.Schema = build_schema(cls, "full", cfg)
    cls.CreateSchema = build_schema(cls, "create", cfg)
    cls.UpdateSchema = build_schema(cls, "update", cfg)
    cls.PublicSchema = build_schema(cls, "public", cfg)
    cls.from_schema = classmethod(_from_schema)
    cls.to_schema = _to_schema
    return cls


@overload
def auto_schema(cls: type[T]) -> type[T]: ...


@overload
def auto_schema(
    cls: None = None,
    *,
    config: SchemaConfig | None = None,
) -> Callable[[type[T]], type[T]]: ...


def auto_schema(cls=None, *, config: SchemaConfig | None = None):
    if cls is not None:
        return _apply_auto_schema(cls, config=config)
    def decorator(klass: type[T]) -> type[T]:
        return _apply_auto_schema(klass, config=config)
    return decorator
