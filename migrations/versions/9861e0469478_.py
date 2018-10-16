"""empty message

Revision ID: 9861e0469478
Revises: 
Create Date: 2018-10-05 01:38:16.290420

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9861e0469478'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('testset',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=80), nullable=False),
    sa.Column('mobile_login', sa.String(length=15), nullable=True),
    sa.Column('password', sa.String(length=256), nullable=False),
    sa.Column('creation_date', sa.DateTime(), nullable=True),
    sa.Column('updation_date', sa.DateTime(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('email_salt', sa.String(length=256), nullable=False),
    sa.Column('confirmed_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('mobile_login')
    )
    op.create_table('userroles',
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('role', sa.String(length=80), nullable=False),
    sa.Column('creation_date', sa.DateTime(), nullable=True),
    sa.Column('updation_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('role_id')
    )
    op.create_table('votetest',
    sa.Column('voteid', sa.Integer(), nullable=False),
    sa.Column('votenumber', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('voteid')
    )
    op.create_table('productmaster',
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('product_title', sa.String(length=1000), nullable=True),
    sa.Column('creation_date', sa.DateTime(), nullable=True),
    sa.Column('updation_date', sa.DateTime(), nullable=True),
    sa.Column('is_live', sa.Boolean(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('soldoff_flag', sa.Boolean(), nullable=True),
    sa.Column('cost_price', sa.Integer(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('product_id')
    )
    op.create_table('useraddress',
    sa.Column('address_id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=True),
    sa.Column('last_name', sa.String(length=50), nullable=True),
    sa.Column('address1', sa.String(length=256), nullable=True),
    sa.Column('address2', sa.String(length=256), nullable=True),
    sa.Column('landmark', sa.String(length=256), nullable=True),
    sa.Column('state', sa.String(length=100), nullable=True),
    sa.Column('city', sa.String(length=75), nullable=True),
    sa.Column('pincode', sa.String(length=10), nullable=True),
    sa.Column('mobileno', sa.String(length=15), nullable=True),
    sa.Column('default_flag', sa.Boolean(), nullable=True),
    sa.Column('delete_flag', sa.Boolean(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('address_id')
    )
    op.create_table('userprofile',
    sa.Column('profile_id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=True),
    sa.Column('last_name', sa.String(length=50), nullable=True),
    sa.Column('gender', sa.String(length=6), nullable=True),
    sa.Column('mobile_number', sa.String(length=15), nullable=True),
    sa.Column('creation_date', sa.DateTime(), nullable=True),
    sa.Column('updation_date', sa.DateTime(), nullable=True),
    sa.Column('dateofbirth', sa.Date(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('profile_id')
    )
    op.create_table('userrolemapping',
    sa.Column('mapping_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['userroles.role_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('mapping_id')
    )
    op.create_table('productimagemapping',
    sa.Column('image_id', sa.Integer(), nullable=False),
    sa.Column('image_name', sa.String(length=200), nullable=True),
    sa.Column('image_path', sa.String(length=512), nullable=True),
    sa.Column('main_image', sa.Boolean(), nullable=True),
    sa.Column('creation_date', sa.DateTime(), nullable=True),
    sa.Column('updation_date', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['productmaster.product_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('image_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('productimagemapping')
    op.drop_table('userrolemapping')
    op.drop_table('userprofile')
    op.drop_table('useraddress')
    op.drop_table('productmaster')
    op.drop_table('votetest')
    op.drop_table('userroles')
    op.drop_table('user')
    op.drop_table('testset')
    # ### end Alembic commands ###