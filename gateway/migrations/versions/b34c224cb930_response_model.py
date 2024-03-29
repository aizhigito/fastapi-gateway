"""response_model

Revision ID: b34c224cb930
Revises: dd39ade2f2df
Create Date: 2023-09-19 14:45:38.235130

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b34c224cb930'
down_revision: Union[str, None] = 'dd39ade2f2df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('fastapi_gateway_scopes', sa.Column('response_model', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('fastapi_gateway_scopes', 'response_model')
    # ### end Alembic commands ###
