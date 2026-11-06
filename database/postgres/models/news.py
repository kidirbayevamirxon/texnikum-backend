from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy import BigInteger,Date,JSON, String,ForeignKey, DateTime,func,Enum as SQLEnum,Text
from enum import Enum as PyEnum
from datetime import datetime
from database.postgres.database import Base





class New(Base):
    __tablename__ = "news"


    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    photo: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    created_date: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_date: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

