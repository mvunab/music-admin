from pymongo import MongoClient, UpdateOne
import os
from dotenv import load_dotenv


load_dotenv() 


MONGO_URI_FROM_ENV = os.getenv("MONGODB_URI")


MONGO_URI = MONGO_URI_FROM_ENV if MONGO_URI_FROM_ENV else "mongodb+srv://Admin:80oqPnKymCOsth2u@cluster0.6dv1ca8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

DATABASE_NAME = "banda_repertorio_db" 
COLLECTION_NAME = "canciones"

if not MONGO_URI or "tu_usuario" in MONGO_URI: 
    print("Error: MONGODB_URI no está configurada correctamente o sigue usando placeholders.")
    print("Por favor, edita el script o asegúrate que tu archivo .env esté accesible y configurado.")
    exit()

print(f"Intentando conectar a MongoDB con URI: {MONGO_URI[:30]}...") 

try:
    client = MongoClient(MONGO_URI)
    client.admin.command('ping')
    print("Conexión a MongoDB exitosa.")
except Exception as e:
    print(f"Error al conectar a MongoDB: {e}")
    exit()

db = client[DATABASE_NAME]
songs_collection = db[COLLECTION_NAME]

print(f"Procesando colección: {db.name}.{songs_collection.name}")

operations = []
documents_processed = 0
documents_to_update_count = 0

for song in songs_collection.find(): # Iterar sobre todos los documentos
    documents_processed += 1
    update_fields = {}
    unset_fields = {} # Para campos que quieres eliminar después de renombrar
    current_id = song["_id"]
    
    print(f"\nRevisando documento ID: {current_id}, Título: {song.get('title', 'N/A')}")

    # 1. Renombrar 'tonality' a 'originalTonality'
    if "tonality" in song:
        if "originalTonality" not in song or song.get("originalTonality") is None: # Solo si no existe o es null
            update_fields["originalTonality"] = song["tonality"]
            unset_fields["tonality"] = "" # Marcar para eliminar el antiguo
            print(f"  - Mapeando 'tonality' ({song['tonality']}) -> 'originalTonality'")
        elif song.get("originalTonality") != song.get("tonality"):
             print(f"  - 'originalTonality' ya existe con valor '{song.get('originalTonality')}', 'tonality' ({song.get('tonality')}) se mantendrá o eliminará si se marca.")
             # Considera si quieres eliminar 'tonality' incluso si 'originalTonality' ya existe
             # unset_fields["tonality"] = ""


    # 2. Renombrar 'lyrics' a 'lyricsWithChords'
    if "lyrics" in song:
        if "lyricsWithChords" not in song or song.get("lyricsWithChords") is None:
            update_fields["lyricsWithChords"] = song["lyrics"]
            unset_fields["lyrics"] = ""
            print(f"  - Mapeando 'lyrics' -> 'lyricsWithChords'")

    # 3. Renombrar 'youtube_link' (snake_case) a 'youtubeLink' (camelCase)
    if "youtube_link" in song:
        if "youtubeLink" not in song or song.get("youtubeLink") is None:
            update_fields["youtubeLink"] = song["youtube_link"]
            unset_fields["youtube_link"] = ""
            print(f"  - Mapeando 'youtube_link' -> 'youtubeLink'")
    
    # 4. Renombrar 'docs_link' (snake_case) a 'docsLink' (camelCase)
    if "docs_link" in song:
        if "docsLink" not in song or song.get("docsLink") is None:
            update_fields["docsLink"] = song["docs_link"]
            unset_fields["docs_link"] = ""
            print(f"  - Mapeando 'docs_link' -> 'docsLink'")
    


    if update_fields: 
        operations.append(UpdateOne({"_id": current_id}, {"$set": update_fields}))
        documents_to_update_count += 1
    
    if unset_fields and update_fields : 
        operations.append(UpdateOne({"_id": current_id}, {"$unset": unset_fields}))


print(f"\nTotal de documentos revisados: {documents_processed}")
if operations:
    print(f"Se prepararon {len(operations)} operaciones para {documents_to_update_count} documentos (un documento puede tener múltiples operaciones si $set y $unset se separan).")
    user_confirmation = input("¿Deseas proceder con estas actualizaciones? (s/N): ")
    if user_confirmation.lower() == 's':
        try:
            result = songs_collection.bulk_write(operations)
            print(f"\nResultado de Bulk Write:")
            print(f"  Documentos insertados: {result.inserted_count}")
            print(f"  Documentos coincidentes para actualización: {result.matched_count}")
            print(f"  Documentos modificados: {result.modified_count}")
            print(f"  Documentos eliminados: {result.deleted_count}")
            print(f"  Documentos actualizados con upsert: {result.upserted_count}")
            print("Migración de datos completada.")
        except Exception as e_bulk:
            print(f"Error durante la escritura en lote (bulk_write): {e_bulk}")
    else:
        print("Operación cancelada por el usuario.")
else:
    print("No se encontraron campos que requieran migración en los documentos existentes o ya están actualizados.")

client.close()
print("Conexión a MongoDB cerrada.")