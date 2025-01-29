"""init

Revision ID: cf803ac77b4d
Revises: 
Create Date: 2025-01-28 18:12:37.065525

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel, utils

# revision identifiers, used by Alembic.
revision: str = 'cf803ac77b4d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('url',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('created_at', utils.datetime.Datetime(), nullable=False),
    sa.Column('updated_at', utils.datetime.Datetime(), nullable=False),
    sa.Column('title', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('original_url', sa.Text(), nullable=False),
    sa.Column('shortlink', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('clicks', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_url_id'), 'url', ['id'], unique=False)
    op.create_index(op.f('ix_url_original_url'), 'url', ['original_url'], unique=False)
    op.create_index(op.f('ix_url_shortlink'), 'url', ['shortlink'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_url_shortlink'), table_name='url')
    op.drop_index(op.f('ix_url_original_url'), table_name='url')
    op.drop_index(op.f('ix_url_id'), table_name='url')
    op.drop_table('url')
    # ### end Alembic commands ###
