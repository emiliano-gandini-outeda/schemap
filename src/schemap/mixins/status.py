from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

class StatusMixin:
    status: Mapped[str] = mapped_column(String(50), default="active")
    
    def activate(self) -> None:
        self.status = "active"
    
    def deactivate(self) -> None:
        self.status = "inactive"

class ArchivableMixin:
    archived_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    
    def archive(self) -> None:
        self.archived_at = datetime.now(timezone.utc)
    
    def restore(self) -> None:
        self.archived_at = None