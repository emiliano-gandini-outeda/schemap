from __future__ import annotations

from typing import Any


def _from_schema(cls: type, schema_obj: Any) -> Any:
    return cls(**schema_obj.model_dump(exclude_none=True))


def _to_schema(self: Any, schema_cls: type | None = None) -> Any:
    if schema_cls is None:
        schema_cls = self.Schema
    return schema_cls.model_validate(self)
