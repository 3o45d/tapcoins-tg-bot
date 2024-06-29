from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database.models.base import Base


class SettingModel(Base):
    __tablename__ = "settings"

    name: Mapped[str] = mapped_column(String, unique=True, primary_key=True, index=True)
    value: Mapped[str] = mapped_column(String, nullable=True)
