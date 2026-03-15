"""create_fit_check_results_table

Revision ID: f1c2d3e4f5a6
Revises: f0b1c2d3e4f5
Create Date: 2026-03-14 05:05:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'f1c2d3e4f5a6'
down_revision: Union[str, Sequence[str], None] = 'f0b1c2d3e4f5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Create the fit_check_results table
    op.create_table(
        'fit_check_results',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('test_session_id', sa.BigInteger(), nullable=False),
        sa.Column('profession_id', sa.BigInteger(), nullable=False),
        sa.Column('user_riasec_code', sa.String(length=10), nullable=True),
        sa.Column('profession_riasec_code', sa.String(length=10), nullable=True),
        sa.Column('match_category', sa.String(length=20), nullable=False),
        sa.Column('rule_type', sa.String(length=50), nullable=True),
        sa.Column('match_score', sa.Float(), nullable=True),
        sa.Column('dominant_letter_same', sa.Boolean(), nullable=True),
        sa.Column('is_adjacent_hexagon', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['test_session_id'], ['careerprofile_test_sessions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Add index
    op.create_index('idx_fit_check_results_session', 'fit_check_results', ['test_session_id'], unique=True)

def downgrade() -> None:
    op.drop_index('idx_fit_check_results_session', table_name='fit_check_results')
    op.drop_table('fit_check_results')
