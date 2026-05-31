# Schemap

Automatic Pydantic v2 schemas from SQLAlchemy 2.0 ORM models: no more manually mirroring your database columns in Pydantic.

> **Note:** This 0.2.0 release provides the core schema generation functionality. Schema configuration and customization are actively being worked on.

```bash
pip install schemap
```

## Quick Start

Define your models with `AutoBase`. Schemas are generated automatically:

```python
from schemap import AutoBase
from sqlalchemy.orm import Mapped, mapped_column

class User(AutoBase):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str]

# Four schemas are available as class attributes:
User.Schema           # all columns
User.CreateSchema     # excludes id, defaults (for inserts)
User.UpdateSchema     # all fields optional (for partial updates)
User.PublicSchema     # excludes fields starting with "__"

# Round-trip between ORM and Pydantic:
data = User.CreateSchema(name="Alice", email="alice@example.com")
user = User.from_schema(data)
schema = user.to_schema()
```

## Standalone Usage

Use `build_schema` without `AutoBase`:

```python
from schemap import build_schema
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

UserSchema = build_schema(User, "default")
```

## Schema Variants

| Variant | Filtering | Nullability |
|---|---|---|
| `"default"` (`.Schema`) | all columns | matches model |
| `"create"` (`.CreateSchema`) | excludes PKs, server_defaults, defaults | matches model |
| `"update"` (`.UpdateSchema`) | excludes PKs | all fields `Optional[type] = None` |
| `"public"` (`.PublicSchema`) | excludes `__`-prefixed columns | matches model |

## Requirements

Python ≥ 3.12.7, SQLAlchemy ≥ 2.0.49, Pydantic ≥ 2.13.4.

## License

MIT
