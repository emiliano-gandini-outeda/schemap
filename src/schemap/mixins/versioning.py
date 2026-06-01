from sqlalchemy.orm import Mapped, mapped_column

class VersionMixin:
    version: Mapped[int] = mapped_column(default=1)
    
    def increment_version(self) -> None:
        self.version += 1