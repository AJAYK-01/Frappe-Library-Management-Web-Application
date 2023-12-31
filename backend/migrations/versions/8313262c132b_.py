"""empty message

Revision ID: 8313262c132b
Revises: 
Create Date: 2023-09-26 14:10:52.533953

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8313262c132b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('books',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('authors', sa.String(), nullable=False),
                    sa.Column('average_rating', sa.Float(), nullable=False),
                    sa.Column('isbn', sa.String(), nullable=False),
                    sa.Column('isbn13', sa.String(), nullable=False),
                    sa.Column('language_code', sa.String(), nullable=False),
                    sa.Column('num_pages', sa.Integer(), nullable=False),
                    sa.Column('ratings_count', sa.Integer(), nullable=False),
                    sa.Column('text_reviews_count',
                              sa.Integer(), nullable=False),
                    sa.Column('publication_date', sa.String(), nullable=False),
                    sa.Column('publisher', sa.String(), nullable=False),
                    sa.Column('stock', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('members',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('outstanding_debt', sa.Float(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('transactions',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('book_id', sa.Integer(), nullable=False),
                    sa.Column('member_id', sa.Integer(), nullable=False),
                    sa.Column('issue_date', sa.Date(), nullable=False),
                    sa.Column('return_date', sa.Date(), nullable=True),
                    sa.Column('rent_fee', sa.Float(), nullable=True),
                    sa.ForeignKeyConstraint(['book_id'], ['books.id'], ),
                    sa.ForeignKeyConstraint(['member_id'], ['members.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transactions')
    op.drop_table('members')
    op.drop_table('books')
    # ### end Alembic commands ###
