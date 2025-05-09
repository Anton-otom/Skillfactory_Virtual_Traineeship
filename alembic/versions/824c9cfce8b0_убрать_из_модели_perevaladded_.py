"""убрать из модели PerevalAdded дублирующее поле date_added

Revision ID: 824c9cfce8b0
Revises: 2d0dd9d7c289
Create Date: 2025-05-02 10:28:45.344504

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '824c9cfce8b0'
down_revision: Union[str, None] = '2d0dd9d7c289'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('pereval_added', 'date_added')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pereval_added', sa.Column('date_added', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
