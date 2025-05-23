"""Consumer and favorities create table

Revision ID: f45fb35200c1
Revises: 5d29436cfe12
Create Date: 2025-05-17 16:42:24.629372

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f45fb35200c1'
down_revision: Union[str, None] = '5d29436cfe12'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Consumers',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Consumers_email'), 'Consumers', ['email'], unique=True)
    op.create_index(op.f('ix_Consumers_id'), 'Consumers', ['id'], unique=False)
    op.create_index(op.f('ix_Consumers_name'), 'Consumers', ['name'], unique=False)
    op.create_table('Favorites',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('consumer_id', sa.UUID(), nullable=False),
    sa.Column('product_id', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['consumer_id'], ['Consumers.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('consumer_id', 'product_id', name='_consumer_product_uc')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Favorites')
    op.drop_index(op.f('ix_Consumers_name'), table_name='Consumers')
    op.drop_index(op.f('ix_Consumers_id'), table_name='Consumers')
    op.drop_index(op.f('ix_Consumers_email'), table_name='Consumers')
    op.drop_table('Consumers')
    # ### end Alembic commands ###
