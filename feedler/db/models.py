# pylint: disable=too-few-public-methods
"""
DB models
"""
import uuid

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from feedler.api.models import ConditionEnum, FieldEnum, MatchResultEnum


class Base(DeclarativeBase):
    """Base db model"""

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)


class Feed(Base):
    """Feed"""

    __tablename__ = "feed"

    url: Mapped[str]
    field: Mapped[FieldEnum]
    condition: Mapped[ConditionEnum]
    matchResult: Mapped[MatchResultEnum]
    query: Mapped[str]
