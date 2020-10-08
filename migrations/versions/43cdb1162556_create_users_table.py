"""create users table

Revision ID: 43cdb1162556
Revises: 
Create Date: 2020-10-08 21:33:28.384023

"""
from alembic import op
from sqlalchemy import Column, Integer, String, Boolean


# revision identifiers, used by Alembic.
revision = '43cdb1162556'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        Column('id', Integer(), primary_key=True, autoincrement=True),
        Column('full_name', String(255)),
        Column('last_name', String(255)),
        Column('first_name', String(255)),
        Column('email', String(255)),
        Column('auth_code', String(255)),
        Column('is_active', Boolean()),
    )


def downgrade():
    op.drop_table('users')