"""fix_fit_check_results_table_v2

Revision ID: f2a3b4c5d6e7
Revises: f1c2d3e4f5a6
Create Date: 2026-03-14 05:10:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f2a3b4c5d6e7'
down_revision: Union[str, Sequence[str], None] = 'f1c2d3e4f5a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # 1. Create the ENUM type for match_category if it doesn't exist
    # Note: We use execute to check existence first
    op.execute("DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'match_category_enum') THEN CREATE TYPE match_category_enum AS ENUM ('HIGH', 'MEDIUM', 'LOW'); END IF; END $$;")

    # 2. Create the fit_check_results table with correct columns
    op.create_table(
        'fit_check_results',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('test_session_id', sa.BigInteger(), nullable=False),
        sa.Column('profession_id', sa.BigInteger(), nullable=False),
        sa.Column('user_riasec_code_id', sa.BigInteger(), nullable=False),
        sa.Column('profession_riasec_code_id', sa.BigInteger(), nullable=False),
        sa.Column('match_category', postgresql.ENUM('HIGH', 'MEDIUM', 'LOW', name='match_category_enum', create_type=False), nullable=False),
        sa.Column('rule_type', sa.String(length=50), nullable=False),
        sa.Column('dominant_letter_same', sa.Boolean(), nullable=False),
        sa.Column('is_adjacent_hexagon', sa.Boolean(), nullable=False),
        sa.Column('match_score', sa.Numeric(precision=4, scale=2), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['test_session_id'], ['careerprofile_test_sessions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Add index
    op.create_index('idx_fit_check_results_session', 'fit_check_results', ['test_session_id'], unique=True)

def downgrade() -> None:
    op.drop_index('idx_fit_check_results_session', table_name='fit_check_results')
    op.drop_table('fit_check_results')
    # op.execute("DROP TYPE IF EXISTS match_category_enum") # Optional: usually keep types
