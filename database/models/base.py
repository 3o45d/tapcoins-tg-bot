
from datetime import datetime
from typing import Annotated

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, mapped_column

created_at = Annotated[datetime, mapped_column(DateTime, default=datetime.utcnow)]


class Base(DeclarativeBase):
    repr_cols_num: int = 3
    repr_cols: tuple = ()

    def __repr__(self) -> str:
        cols = [
            f"{col}={getattr(self, col)}"
            for idx, col in enumerate(self.__table__.columns.keys())
            if col in self.repr_cols or idx < self.repr_cols_num
        ]
        return f"<{self.__class__.__name__} {', '.join(cols)}>"
