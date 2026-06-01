"""Soft delete mixin for marking rows as deleted without removing them."""

from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column

class SoftDeleteMixin:
    """Adds soft delete capability with deleted_at timestamp."""
    
    deleted_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    
    def soft_delete(self) -> None:
        """Mark this instance as deleted."""
        self.deleted_at = datetime.now(timezone.utc)
    
    @classmethod
    def active(cls):
        """Return query filter for undeleted records."""
        return cls.deleted_at.is_(None)