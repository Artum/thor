"""first init

Revision ID: 43cdb1162556
Revises: 
Create Date: 2020-10-08 21:33:28.384023

"""
from alembic import op
from sqlalchemy import Column
from sqlalchemy.types import Integer, String, Boolean, DateTime, Float
from sqlalchemy.sql import func



# revision identifiers, used by Alembic.
revision = '43cdb1162556'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user",
        Column('user_id', String(256), primary_key=True),
        Column('full_name', String(256)),
        Column('first_name', String(256)),
        Column('last_name', String(256)),
        Column('email', String(512)),
        Column('token', String(512)),
    )
    op.create_table(
        "document",
        Column('id', String(256), primary_key=True),
        Column('user_id', String(256), primary_key=True),
    )

def downgrade():
    op.drop_table('document')
    op.drop_table('user')