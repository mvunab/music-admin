"""
Script de utilidad para reiniciar y preparar el entorno de desarrollo.
Este script realiza las siguientes tareas:
1. Verifica la estructura de la base de datos y aplica correcciones si es necesario
2. Verifica la compatibilidad de los valores de enum
3. Ejecuta la aplicación en modo de desarrollo
"""
import os
import sys
import subprocess
from pathlib import Path

# Añadir el directorio raíz al PYTHONPATH
root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(root_dir))

def run_script(script_path):
    """
    Ejecuta un script Python.
    
    Args:
        script_path (str): Ruta al script Python a ejecutar.
    """
    print(f"\n{'='*80}")
    print(f"Ejecutando {script_path}")
    print(f"{'='*80}\n")
    
    result = subprocess.run([sys.executable, script_path], check=False)
    
    if result.returncode != 0:
        print(f"\n❌ El script {script_path} falló con código de salida {result.returncode}")
        return False
    
    print(f"\n✅ Script {script_path} ejecutado con éxito")
    return True

def setup_dev_environment():
    """
    Configura el entorno de desarrollo.
    """
    # Ruta a los scripts de utilidad
    fix_db_script = os.path.join(root_dir, "backend", "utils", "fix_database.py")
    check_enum_script = os.path.join(root_dir, "backend", "utils", "enum_checker.py")
    
    # Verificar y corregir la estructura de la base de datos
    if not run_script(fix_db_script):
        print("No se pudo corregir la estructura de la base de datos. Abortando.")
        return False
    
    # Verificar la compatibilidad de los valores de enum
    if not run_script(check_enum_script):
        print("Se encontraron problemas con los valores de enum. Revise el código y la base de datos.")
        return False
    
    print("\n✅ Entorno de desarrollo configurado correctamente")
    return True

if __name__ == "__main__":
    if setup_dev_environment():
        # Ruta al script de ejecución de la aplicación
        run_app_script = os.path.join(root_dir, "run_app.py")
        
        print("\n¿Desea iniciar la aplicación? (S/n): ", end="")
        response = input().strip().lower()
        
        if response in ["", "s", "si", "sí", "y", "yes"]:
            print("\nIniciando la aplicación...")
            # Ejecutar la aplicación
            subprocess.run([sys.executable, run_app_script])
        else:
            print("\nNo se iniciará la aplicación.")
    else:
        print("\n❌ No se pudo configurar el entorno de desarrollo correctamente.")
