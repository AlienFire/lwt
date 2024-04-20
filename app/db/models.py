from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

from datetime import datetime

Base = declarative_base()


class Content(Base):
    __tablename__ = "content"
    id = Column(Integer, primary_key=True)
    name = Column(String(200), unique=True)
    created_at = Column(
        DateTime,
        default=datetime.now,
    )


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(
        "id",
        Integer,
        primary_key=True,
    )
    username: Mapped[str] = mapped_column(
        "username",
        String(200),
        unique=True,
    )
    password: Mapped[str] = mapped_column("password", String)
    created_at: Mapped[datetime] = mapped_column(
        "created_at",
        DateTime,
        default=datetime.now,
    )
