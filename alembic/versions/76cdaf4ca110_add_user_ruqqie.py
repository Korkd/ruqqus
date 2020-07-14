"""Add user ruqqie

Revision ID: 76cdaf4ca110
Revises: 01bcc5ec8808
Create Date: 2020-07-13 22:34:51.322051

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76cdaf4ca110'
down_revision = '01bcc5ec8808'
branch_labels = None
depends_on = None


def upgrade():
    users = sa.table('users',
                     sa.column('id', sa.Integer()),
                     sa.column('username', sa.String(length=255)),
                     sa.column('email', sa.String(length=255)),
                     sa.column('passhash', sa.String(length=255)),
                     sa.column('created_utc', sa.Integer()),
                     sa.column('admin_level', sa.Integer()),
                     sa.column('creation_ip', sa.String(length=255)),
                     sa.column('login_nonce', sa.Integer()),
                     sa.column('tos_agreed_utc', sa.Integer())
                     )

    op.execute(users.insert().values(
        username='ruqqie',
        email='ruqqie@ruqqus.com',
        passhash='pbkdf2:sha512:150000$vmPzuBFj$24cde8a6305b7c528b0428b1e87f256c65741bb035b4356549c13e745cc0581701431d5a2297d98501fcf20367791b4334dcd19cf063a6e60195abe8214f91e8',
        created_utc='1592672337',
        creation_ip='127.0.0.1',
        tos_agreed_utc='1592672337',
        login_nonce='1'
    ))


def downgrade():
    op.execute("DELETE FROM users WHERE username = 'ruqqie';")
    pass
