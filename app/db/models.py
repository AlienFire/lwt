from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship

from datetime import datetime

Base = declarative_base()


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
    notes: Mapped["list[Notebook]"] = relationship(
        "Notebook",
        back_populates="author",
    )
    content: Mapped["list[Content]"] = relationship(
        "Content",
        back_populates="author",
    )


class Content(Base):
    __tablename__ = "content"
    id: Mapped[int] = mapped_column(
        "id",
        Integer,
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(
        "name",
        String(200),
        unique=True,
    )
    created_at: Mapped[DateTime] = mapped_column(
        "created_at",
        DateTime,
        default=datetime.now,
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "user.id",
        ),
    )

    author: Mapped[User] = relationship(
        "User",
        back_populates="content",
    )


class Notebook(Base):
    __tablename__ = "notebook"
    id: Mapped[int] = mapped_column(
        "id",
        Integer,
        primary_key=True,
    )
    header: Mapped[str] = mapped_column(
        "header",
        String(300),
    )
    note: Mapped[str] = mapped_column(
        "note",
        String,
    )
    date: Mapped[datetime] = mapped_column("date", DateTime, default=datetime.now())
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user.id"),
    )
    author: Mapped[User] = relationship(
        "User",
        back_populates="notes",
    )
