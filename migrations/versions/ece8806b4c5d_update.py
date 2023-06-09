"""update

Revision ID: ece8806b4c5d
Revises: f88f03273d19
Create Date: 2023-04-04 22:51:33.133584

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ece8806b4c5d'
down_revision = 'f88f03273d19'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('groups',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('group_name', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_groups'))
    )
    op.create_index(op.f('ix_groups_id'), 'groups', ['id'], unique=False)
    op.create_table('patientgroups',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], name=op.f('fk_patientgroups_group_id_groups')),
    sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], name=op.f('fk_patientgroups_patient_id_patients')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_patientgroups'))
    )
    op.create_index(op.f('ix_patientgroups_id'), 'patientgroups', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_patientgroups_id'), table_name='patientgroups')
    op.drop_table('patientgroups')
    op.drop_index(op.f('ix_groups_id'), table_name='groups')
    op.drop_table('groups')
    # ### end Alembic commands ###
