from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

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
