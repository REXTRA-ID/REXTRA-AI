"""Alter result tables

Revision ID: 344b3dbd502c
Revises: 103c49642de4
Create Date: 2026-02-23 16:36:48.288575

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '344b3dbd502c'
down_revision: Union[str, Sequence[str], None] = '103c49642de4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. ALTER TABLE career_recommendations
    op.execute("""
        ALTER TABLE career_recommendations
        ADD COLUMN IF NOT EXISTS top_profession1_id BIGINT,
        ADD COLUMN IF NOT EXISTS top_profession2_id BIGINT,
        ADD COLUMN IF NOT EXISTS ai_model_used VARCHAR(50) DEFAULT 'gemini-1.5-flash'
    """)


def downgrade() -> None:
    # 1. Hapus 3 kolom yang ditambahkan ke career_recommendations
    # Note: downgrade normally drops the columns
    op.drop_column("career_recommendations", "ai_model_used")
    op.drop_column("career_recommendations", "top_profession2_id")
    op.drop_column("career_recommendations", "top_profession1_id")
