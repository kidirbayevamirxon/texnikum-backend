from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy import BigInteger,Date,JSON,Text, String,ForeignKey, DateTime,func,Enum as SQLEnum
from enum import Enum as PyEnum
from datetime import datetime
from database.postgres.database import Base



class Deficiency(Base):
    __tablename__ = "deficiencies"


    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    photo: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,   # upload bo‘lsa keladi
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
