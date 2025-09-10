"""add_target_and_initial_grade_to_student

Revision ID: b1c2d3e4f5a6
Revises: 0ad5a6c491fc
Create Date: 2025-09-03 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1c2d3e4f5a6'
down_revision = '0ad5a6c491fc'
branch_labels = None
depends_on = None


def upgrade():
    # Добавляем новые поля для ОГЭ в таблицу student
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.add_column(sa.Column('target_grade', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('initial_grade', sa.Integer(), nullable=True))


def downgrade():
    # Удаляем добавленные поля
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.drop_column('initial_grade')
        batch_op.drop_column('target_grade')


