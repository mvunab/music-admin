from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from typing import List, Any 
from bson import ObjectId

from backend.schemas_song import SongCreate, SongUpdate, SongInDB 
from backend.db_mongo import get_song_collection

router = APIRouter(
    tags=["Canciones"],
)


def format_song_for_frontend(song_doc: dict) -> dict:
    return {
        "id": str(song_doc["_id"]),
        "title": song_doc.get("title"),
        "category": song_doc.get("category"),
        "originalTonality": song_doc.get("originalTonality") or song_doc.get("tonality"), 
        "bpm": song_doc.get("bpm"),
        "youtubeLink": str(song_doc.get("youtubeLink") or song_doc.get("youtube_link")) if (song_doc.get("youtubeLink") or song_doc.get("youtube_link")) else None,
        "docsLink": str(song_doc.get("docsLink") or song_doc.get("docs_link")) if (song_doc.get("docsLink") or song_doc.get("docs_link")) else None,
        "lyricsWithChords": song_doc.get("lyricsWithChords") or song_doc.get("lyrics") 
    }

@router.post("/", response_model=SongInDB, status_code=status.HTTP_201_CREATED)
async def create_song(song_data: SongCreate): 
    collection = get_song_collection()
    song_dict_to_insert = song_data.model_dump(exclude_unset=True) 
    
    if song_dict_to_insert.get("category") not in ["REP", "PROP"]:
        raise HTTPException(status_code=400, detail="Categoría inválida. Debe ser 'REP' o 'PROP'.")
    if not song_dict_to_insert.get("originalTonality"): 
         raise HTTPException(status_code=400, detail="La tonalidad original es requerida.")

    result = await collection.insert_one(song_dict_to_insert)
    new_song_doc = await collection.find_one({"_id": result.inserted_id})
    if new_song_doc:
        return new_song_doc 
    raise HTTPException(status_code=400, detail="No se pudo crear la canción.")

@router.get("/", response_model=None) 
async def read_songs(skip: int = 0, limit: int = 100) -> JSONResponse:
    collection = get_song_collection()
    songs_to_return = []
    songs_cursor = collection.find().skip(skip).limit(limit)
    async for song_doc in songs_cursor:
        songs_to_return.append(format_song_for_frontend(song_doc))
    return JSONResponse(content=songs_to_return)

@router.get("/{song_id}", response_model=SongInDB)
async def read_song(song_id: str):
    collection = get_song_collection()
    try:
        obj_id = ObjectId(song_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID de canción inválido.")
    
    song_doc = await collection.find_one({"_id": obj_id})
    if song_doc:
        
        return song_doc
    raise HTTPException(status_code=404, detail=f"Canción con id {song_id} no encontrada.")

@router.put("/{song_id}", response_model=SongInDB)
async def update_song(song_id: str, song_data: SongUpdate):
    collection = get_song_collection()
    try:
        obj_id = ObjectId(song_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID de canción inválido.")
    
    update_values = song_data.model_dump(exclude_unset=True) 

    if not update_values:
        raise HTTPException(status_code=400, detail="No hay datos para actualizar.")
    if "category" in update_values and update_values["category"] not in ["REP", "PROP"]:
         raise HTTPException(status_code=400, detail="Categoría inválida. Debe ser 'REP' o 'PROP'.")
    if "originalTonality" in update_values and not update_values["originalTonality"]:
        raise HTTPException(status_code=400, detail="La tonalidad original no puede estar vacía si se actualiza explícitamente.")


    result = await collection.update_one({"_id": obj_id}, {"$set": update_values})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail=f"Canción con id {song_id} no encontrada.")
    
    updated_song_doc = await collection.find_one({"_id": obj_id})
    if updated_song_doc:
        return updated_song_doc
    raise HTTPException(status_code=404, detail=f"Canción con id {song_id} no encontrada después de la actualización.")

@router.delete("/{song_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_song(song_id: str):
    collection = get_song_collection()
    try:
        obj_id = ObjectId(song_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID de canción inválido.")
    result = await collection.delete_one({"_id": obj_id})
    if result.deleted_count == 1:
        return
    raise HTTPException(status_code=404, detail=f"Canción con id {song_id} no encontrada.")