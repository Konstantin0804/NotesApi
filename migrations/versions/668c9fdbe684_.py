"""empty message

Revision ID: 668c9fdbe684
Revises: 
Create Date: 2021-09-15 16:45:01.903260

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import expression

# revision identifiers, used by Alembic.
revision = '668c9fdbe684'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_model',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=32), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('is_staff', sa.Boolean(), server_default=expression.false(), nullable=False),
    sa.Column('role', sa.String(length=32), server_default='admin', nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('note_model',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('text', sa.String(length=255), nullable=False),
    sa.Column('private', sa.Boolean(), server_default=expression.true(), nullable=False),
    sa.Column('archive', sa.Boolean(), server_default=expression.false(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['user_model.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('author', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['author'], ['user_model.username'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('tags',
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('note_model_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['note_model_id'], ['note_model.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], ),
    sa.PrimaryKeyConstraint('tag_id', 'note_model_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tags')
    op.drop_table('tag')
    op.drop_table('note_model')
    op.drop_table('user_model')
    # ### end Alembic commands ###
