"""
Script para realizar pruebas básicas de la API.
Este script verifica que los endpoints principales de la API estén funcionando correctamente.
"""
import os
import sys
import requests
import json
from pathlib import Path

# Añadir el directorio raíz al PYTHONPATH
root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(root_dir))

# URL base de la API
API_BASE_URL = "http://localhost:8000"

def test_endpoint(endpoint, method="GET", data=None, token=None):
    """
    Prueba un endpoint de la API.
    
    Args:
        endpoint (str): Endpoint a probar.
        method (str, optional): Método HTTP a utilizar. Por defecto es "GET".
        data (dict, optional): Datos a enviar en la petición. Por defecto es None.
        token (str, optional): Token de autenticación. Por defecto es None.
        
    Returns:
        tuple: (Código de estado HTTP, Respuesta JSON)
    """
    url = f"{API_BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method == "PUT":
            response = requests.put(url, headers=headers, json=data)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            print(f"Método HTTP no soportado: {method}")
            return None, None
        
        try:
            json_response = response.json()
        except:
            json_response = {"text": response.text}
        
        return response.status_code, json_response
    except requests.RequestException as e:
        print(f"Error al realizar la petición: {e}")
        return None, None

def run_api_tests():
    """
    Ejecuta pruebas básicas de la API.
    """
    print("Iniciando pruebas de la API...")
    
    # Probar el endpoint raíz
    status, response = test_endpoint("/")
    print(f"\n1. Endpoint raíz ('/')")
    print(f"   Código de estado: {status}")
    print(f"   Respuesta: {json.dumps(response, indent=2, ensure_ascii=False)}")
    
    # Probar el endpoint de autenticación
    login_data = {
        "username": "user@example.com",
        "password": "password123"
    }
    status, response = test_endpoint("/token", method="POST", data=login_data)
    print(f"\n2. Endpoint de autenticación ('/token')")
    print(f"   Código de estado: {status}")
    print(f"   Respuesta: {json.dumps(response, indent=2, ensure_ascii=False)}")
    
    # Almacenar el token si la autenticación fue exitosa
    token = response.get("access_token") if status == 200 else None
    
    # Probar el endpoint de usuarios
    status, response = test_endpoint("/usuarios/", token=token)
    print(f"\n3. Endpoint de usuarios ('/usuarios/')")
    print(f"   Código de estado: {status}")
    print(f"   Respuesta: {json.dumps(response, indent=2, ensure_ascii=False)}")
    
    # Probar el endpoint de roles musicales
    status, response = test_endpoint("/roles_musicales/", token=token)
    print(f"\n4. Endpoint de roles musicales ('/roles_musicales/')")
    print(f"   Código de estado: {status}")
    print(f"   Respuesta: {json.dumps(response, indent=2, ensure_ascii=False)}")
    
    print("\nPruebas de API completadas.")

if __name__ == "__main__":
    run_api_tests()
