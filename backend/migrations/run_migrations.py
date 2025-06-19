"""Script para ejecutar migraciones de Alembic

Este script permite ejecutar las migraciones de Alembic desde la línea de comandos.
"""

import os
import sys
from alembic.config import Config
from alembic import command

def run_migrations(action='upgrade', revision='head'):
    """Ejecuta migraciones de Alembic
    
    Args:
        action (str): Acción a ejecutar (upgrade, downgrade, etc.)
        revision (str): Revisión objetivo (head, -1, etc.)
    """
    # Configura Alembic usando el archivo alembic.ini
    alembic_cfg = Config(os.path.join(os.path.dirname(__file__), '../../alembic.ini'))
    
    # Ejecuta la acción correspondiente
    if action == 'upgrade':
        command.upgrade(alembic_cfg, revision)
    elif action == 'downgrade':
        command.downgrade(alembic_cfg, revision)
    elif action == 'revision':
        command.revision(alembic_cfg, autogenerate=True, message=revision)
    else:
        print(f"Acción no reconocida: {action}")
        sys.exit(1)

if __name__ == "__main__":
    # Obtiene los argumentos de la línea de comandos
    if len(sys.argv) < 2:
        print("Uso: python run_migrations.py [upgrade|downgrade|revision] [revision]")
        sys.exit(1)
    
    action = sys.argv[1]
    revision = sys.argv[2] if len(sys.argv) > 2 else 'head'
    
    run_migrations(action, revision)
