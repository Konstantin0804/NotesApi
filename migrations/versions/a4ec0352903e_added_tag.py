"""added tag

Revision ID: a4ec0352903e
Revises: 17218d474bda
Create Date: 2021-09-09 21:55:21.644040

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4ec0352903e'
down_revision = '17218d474bda'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
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
    # ### end Alembic commands ###