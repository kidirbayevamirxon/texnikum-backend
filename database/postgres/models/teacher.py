from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy import BigInteger,Date,JSON, String,ForeignKey, DateTime,func,Enum as SQLEnum
from enum import Enum as PyEnum
from datetime import datetime
from database.postgres.database import Base




class Teacher(Base):
    __tablename__ = "teachers"


    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)

    middle_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    photo: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )
