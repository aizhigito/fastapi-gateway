"""make group unique

Revision ID: 89c0b1e53a97
Revises: b34c224cb930
Create Date: 2023-09-20 16:22:11.182080

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '89c0b1e53a97'
down_revision: Union[str, None] = 'b34c224cb930'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('fastapi_gateway_scopes', schema=None) as batch_op:
        batch_op.create_unique_constraint('unique_microservice_path', ['microservice_id', 'microservice_path', 'method'])
        batch_op.create_unique_constraint('unique_path', ['path', 'method'])

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('fastapi_gateway_scopes', schema=None) as batch_op:
        batch_op.drop_constraint('unique_path', type_='unique')
        batch_op.drop_constraint('unique_microservice_path', type_='unique')

    # ### end Alembic commands ###
