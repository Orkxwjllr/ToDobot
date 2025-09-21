from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, BigInteger, Boolean, Integer

from app.infrastructure.connection.base import Base

class TaskBase(Base):
    __tablename__ = "taskname"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    task: Mapped[str] = mapped_column(String(1500), nullable=False)
    is_done: Mapped[bool] = mapped_column(Boolean, default=False)