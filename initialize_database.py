"""Script para inicializar la base de datos

Este script crea las tablas en la base de datos si no existen y ejecuta las migraciones pendientes.
"""

import os
import sys
from backend.database import Base, engine
from backend import models
from backend.migrations.run_migrations import run_migrations

def initialize_database():
    """Inicializa la base de datos y ejecuta migraciones pendientes"""
    # Crea las tablas si no existen
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas en la base de datos.")
    
    # Ejecuta las migraciones pendientes
    run_migrations('upgrade', 'head')
    print("Migraciones ejecutadas correctamente.")

if __name__ == "__main__":
    initialize_database()
