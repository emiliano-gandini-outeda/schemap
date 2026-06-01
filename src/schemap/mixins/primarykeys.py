from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID, uuid4

class UUIDPrimaryKeyMixin:
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

class IntPrimaryKeyMixin:
    id: Mapped[int] = mapped_column(primary_key=True)