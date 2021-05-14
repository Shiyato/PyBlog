"""empty message

Revision ID: ffd555b8b0ea
Revises: aaee1e13c66d
Create Date: 2021-05-13 20:55:33.010200

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ffd555b8b0ea'
down_revision = 'aaee1e13c66d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('coment_likes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), ),
    sa.Column('coment_id', sa.Integer(), ),
    sa.ForeignKeyConstraint(['coment_id'], ['posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('post_likes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), ),
    sa.Column('post_id', sa.Integer(), ),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('saves',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), ),
    sa.Column('post_id', sa.Integer(), ),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_column('coments', 'likes')
    op.drop_column('posts', 'likes')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('likes', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('coments', sa.Column('likes', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_table('saves')
    op.drop_table('post_likes')
    op.drop_table('coment_likes')
    # ### end Alembic commands ###
