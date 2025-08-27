"""add_rol_musical_id_to_asignaciones

Revision ID: 81ad86706a64
Revises: 
Create Date: 2023-07-08 23:45:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81ad86706a64'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Añadir columna rol_musical_id a la tabla asignaciones
    op.add_column('asignaciones',
        sa.Column('rol_musical_id', sa.Integer(unsigned=True), nullable=True)
    )
    # Crear índice para mejorar el rendimiento
    op.create_index(op.f('ix_asignaciones_rol_musical_id'), 'asignaciones', ['rol_musical_id'], unique=False)
    # Añadir restricción de clave foránea
    op.create_foreign_key('fk_rol_musical', 'asignaciones', 'roles_musicales', ['rol_musical_id'], ['id'])


def downgrade():
    # Eliminar restricción de clave foránea
    op.drop_constraint('fk_rol_musical', 'asignaciones', type_='foreignkey')
    # Eliminar índice
    op.drop_index(op.f('ix_asignaciones_rol_musical_id'), table_name='asignaciones')
    # Eliminar columna
    op.drop_column('asignaciones', 'rol_musical_id')