from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy import BigInteger,Date,JSON, String,ForeignKey, DateTime,func,Enum as SQLEnum
from enum import Enum as PyEnum
from datetime import datetime
from database.postgres.database import Base



class User(Base):
    __tablename__ = "users"
    
    login: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)

