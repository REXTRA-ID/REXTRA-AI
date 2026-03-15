"""create_user_career_profile_table

Revision ID: f0b1c2d3e4f5
Revises: eb8dc7fda46a
Create Date: 2026-03-14 04:30:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f0b1c2d3e4f5'
down_revision: Union[str, Sequence[str], None] = 'a7b943637d93'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Create the user_career_profiles table
    op.create_table(
        'user_career_profiles',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('test_session_id', sa.BigInteger(), nullable=False),
        sa.Column('top_profession1_id', sa.BigInteger(), nullable=True),
        sa.Column('top_profession2_id', sa.BigInteger(), nullable=True),
        sa.Column('riasec_code', sa.String(length=6), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('activated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['test_session_id'], ['careerprofile_test_sessions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Add indexes for faster querying
    op.create_index('idx_user_career_profiles_user_id', 'user_career_profiles', ['user_id'], unique=False)
    op.create_index('idx_user_career_profiles_session_id', 'user_career_profiles', ['test_session_id'], unique=False)
    op.create_index('idx_user_career_profiles_user_active', 'user_career_profiles', ['user_id', 'is_active'], unique=False)

def downgrade() -> None:
    # Drop indexes first
    op.drop_index('idx_user_career_profiles_user_active', table_name='user_career_profiles')
    op.drop_index('idx_user_career_profiles_session_id', table_name='user_career_profiles')
    op.drop_index('idx_user_career_profiles_user_id', table_name='user_career_profiles')
    
    # Drop the table
    op.drop_table('user_career_profiles')
