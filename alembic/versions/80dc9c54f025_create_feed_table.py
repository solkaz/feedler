"""create feed table

Revision ID: 80dc9c54f025
Revises:
Create Date: 2023-10-30 17:19:06.327588

"""
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM as pgEnum
from sqlalchemy.dialects.postgresql import UUID

from alembic import op
from feedler.api.models import ConditionEnum, FieldEnum, MatchResultEnum

# revision identifiers, used by Alembic.
revision: str = "80dc9c54f025"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(  # type: ignore
        "feed",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("url", sa.String(50), nullable=False),
        sa.Column("field", pgEnum(FieldEnum)),
        sa.Column("condition", pgEnum(ConditionEnum)),
        sa.Column("matchResult", pgEnum(MatchResultEnum)),
        sa.Column("query", sa.Unicode(200)),
    )


def downgrade() -> None:
    pass
