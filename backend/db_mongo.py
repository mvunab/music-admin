from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv() 

MONGO_DETAILS = os.getenv("MONGODB_URI")

if not MONGO_DETAILS:
    raise ValueError("La variable de entorno MONGODB_URI no está configurada.")

class Database:
    client: AsyncIOMotorClient = None

db = Database()

async def connect_to_mongo():
    print(f"Intentando conectar a MongoDB Atlas...")
    db.client = AsyncIOMotorClient(MONGO_DETAILS, server_api=ServerApi('1'))
    try:
        await db.client.admin.command('ping')
        print("Ping exitoso. Conectado a MongoDB Atlas!")
    except Exception as e:
        print(f"Error al conectar o hacer ping a MongoDB: {e}")


async def close_mongo_connection():
    if db.client:
        print("Cerrando conexión con MongoDB.")
        db.client.close()

def get_song_collection():
    if not db.client:
        raise Exception("Cliente MongoDB no inicializado. Llama a connect_to_mongo primero.")
    return db.client.banda_repertorio_db.canciones 