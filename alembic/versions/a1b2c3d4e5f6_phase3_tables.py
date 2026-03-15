"""phase3_tables

Revision ID: a1b2c3d4e5f6
Revises: 97caa26d93fb
Create Date: 2026-02-21 20:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = '97caa26d93fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create Phase 3 tables: fit_check_results and career_recommendations."""

    # Create the ENUM type for match_category
    op.execute("CREATE TYPE match_category_enum AS ENUM ('HIGH', 'MEDIUM', 'LOW')")

    # Create fit_check_results table
    op.create_table(
        'fit_check_results',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('test_session_id', sa.BigInteger(), nullable=False),
        sa.Column(
            'match_category',
            postgresql.ENUM('HIGH', 'MEDIUM', 'LOW', name='match_category_enum', create_type=False),
            nullable=False
        ),
        sa.Column('rule_type', sa.String(length=50), nullable=False),
        sa.Column('match_score', sa.Numeric(4, 2), nullable=True),
        sa.Column('generated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['test_session_id'], ['careerprofile_test_sessions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('test_session_id')
    )

    # Create career_recommendations table
    op.create_table(
        'career_recommendations',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('test_session_id', sa.BigInteger(), nullable=False),
        sa.Column(
            'recommendations_data',
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False
        ),
        sa.Column('generated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['test_session_id'], ['careerprofile_test_sessions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('test_session_id')
    )

    # Add scores_data column to riasec_results if it's not there yet
    # (used by result_service to check riasec_res.scores_data)
    op.add_column(
        'riasec_results',
        sa.Column('scores_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True)
    )
    op.add_column(
        'riasec_results',
        sa.Column('riasec_code', sa.String(length=3), nullable=True)
    )


def downgrade() -> None:
    """Remove Phase 3 tables."""
    op.drop_column('riasec_results', 'riasec_code')
    op.drop_column('riasec_results', 'scores_data')
    op.drop_table('career_recommendations')
    op.drop_table('fit_check_results')
    op.execute("DROP TYPE IF EXISTS match_category_enum")
