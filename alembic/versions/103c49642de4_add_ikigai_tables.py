"""Add Ikigai tables

Revision ID: 103c49642de4
Revises: d364c74c43e5
Create Date: 2026-02-23 16:31:29.158689

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '103c49642de4'
down_revision: Union[str, Sequence[str], None] = 'd364c74c43e5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. CREATE TABLE ikigai_responses
    op.create_table(
        "ikigai_responses",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column(
            "test_session_id",
            sa.BigInteger(),
            sa.ForeignKey("careerprofile_test_sessions.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column("dimension_1_love",        postgresql.JSONB(), nullable=True),
        sa.Column("dimension_2_good_at",     postgresql.JSONB(), nullable=True),
        sa.Column("dimension_3_world_needs", postgresql.JSONB(), nullable=True),
        sa.Column("dimension_4_paid_for",    postgresql.JSONB(), nullable=True),
        sa.Column("completed",    sa.Boolean(), nullable=False, server_default="false"),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("completed_at", sa.TIMESTAMP(timezone=True), nullable=True),
    )
    op.create_index(
        "ix_ikigai_responses_test_session_id",
        "ikigai_responses",
        ["test_session_id"],
    )

    # 2. CREATE TABLE ikigai_dimension_scores
    op.create_table(
        "ikigai_dimension_scores",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column(
            "test_session_id",
            sa.BigInteger(),
            sa.ForeignKey("careerprofile_test_sessions.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column("scores_data",     postgresql.JSONB(), nullable=False),
        sa.Column(
            "calculated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("ai_model_used",   sa.String(50),  nullable=True, server_default="gemini-1.5-flash"),
        sa.Column("total_api_calls", sa.Integer(),   nullable=True, server_default="4"),
        sa.CheckConstraint(
            "total_api_calls BETWEEN 1 AND 20",
            name="chk_valid_api_calls",
        ),
    )
    op.create_index(
        "ix_ikigai_dimension_scores_test_session_id",
        "ikigai_dimension_scores",
        ["test_session_id"],
    )

    # 3. CREATE TABLE ikigai_total_scores
    op.create_table(
        "ikigai_total_scores",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column(
            "test_session_id",
            sa.BigInteger(),
            sa.ForeignKey("careerprofile_test_sessions.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column("scores_data",         postgresql.JSONB(), nullable=False),
        sa.Column("top_profession_1_id", sa.BigInteger(), nullable=True),
        sa.Column("top_profession_2_id", sa.BigInteger(), nullable=True),
        sa.Column(
            "calculated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "top_profession_1_id IS NULL OR top_profession_2_id IS NULL OR "
            "top_profession_1_id != top_profession_2_id",
            name="chk_different_top_professions",
        ),
    )
    op.create_index(
        "ix_ikigai_total_scores_test_session_id",
        "ikigai_total_scores",
        ["test_session_id"],
    )

    # 4. ALTER TABLE ikigai_candidate_professions
    op.execute("""
        ALTER TABLE ikigai_candidate_professions
        ADD COLUMN IF NOT EXISTS total_candidates BIGINT,
        ADD COLUMN IF NOT EXISTS generation_strategy VARCHAR(50),
        ADD COLUMN IF NOT EXISTS max_candidates_limit INTEGER DEFAULT 30
    """)


def downgrade() -> None:
    # 4. Hapus kolom yang ditambahkan ke ikigai_candidate_professions
    op.drop_column("ikigai_candidate_professions", "max_candidates_limit")
    op.drop_column("ikigai_candidate_professions", "generation_strategy")
    op.drop_column("ikigai_candidate_professions", "total_candidates")

    # 3. Drop ikigai_total_scores
    op.drop_index(
        "ix_ikigai_total_scores_test_session_id",
        table_name="ikigai_total_scores",
    )
    op.drop_table("ikigai_total_scores")

    # 2. Drop ikigai_dimension_scores
    op.drop_index(
        "ix_ikigai_dimension_scores_test_session_id",
        table_name="ikigai_dimension_scores",
    )
    op.drop_table("ikigai_dimension_scores")

    # 1. Drop ikigai_responses
    op.drop_index(
        "ix_ikigai_responses_test_session_id",
        table_name="ikigai_responses",
    )
    op.drop_table("ikigai_responses")
