# Schemap

Automatic Pydantic v2 schemas from SQLAlchemy 2.0 ORM models.

```bash
pip install schemap
```

## Quick Start

```python
from schemap import AutoBase
from sqlalchemy.orm import Mapped, mapped_column

class User(AutoBase):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str]

User.Schema         # all columns
User.CreateSchema   # excludes PKs, server_defaults, defaults
User.UpdateSchema   # all fields Optional (partial updates)
User.PublicSchema   # excludes __-prefixed fields

# Round-trip ORM <-> Pydantic
data = User.CreateSchema(name="Alice", email="alice@example.com")
user = User.from_schema(data)
schema = user.to_schema()
```

## SchemaConfig

Customize generated schemas per model using `__schema_config__`:

```python
from schemap import AutoBase
from schemap.config import SchemaConfig
from sqlalchemy.orm import Mapped, mapped_column

class User(AutoBase):
    __tablename__ = "users"
    __schema_config__ = SchemaConfig(
        exclude_public=["email"],
        exclude_create=["internal_id"],
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str]
    internal_id: Mapped[int]
```

| Option | Type | Description |
|---|---|---|
| `exclude_always` | `list[str]` | Exclude from all schema variants |
| `exclude_create` | `list[str]` | Exclude from CreateSchema only |
| `exclude_update` | `list[str]` | Exclude from UpdateSchema only |
| `exclude_public` | `list[str]` | Exclude from PublicSchema only |
| `field_overrides` | `dict[str, Any]` | Override a field's Python type |
| `required_always` | `list[str]` | Force fields to be required |
| `optional_always` | `list[str]` | Force fields to be optional |

## Standalone

```python
from schemap import build_schema
from schemap.config import SchemaConfig

UserSchema = build_schema(User, "create", config=SchemaConfig(exclude_create=["internal_id"]))
```

## Requirements

Python ≥ 3.12.7, SQLAlchemy ≥ 2.0.49, Pydantic ≥ 2.13.4.

## License

MIT
