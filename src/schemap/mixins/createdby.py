from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import ForeignKey

class CreatedByMixin:
    created_by_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    created_by: Mapped[Optional["User"]] = relationship()  # noqa: F821

class UpdatedByMixin:
    updated_by_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    updated_by: Mapped[Optional["User"]] = relationship()  # noqa: F821