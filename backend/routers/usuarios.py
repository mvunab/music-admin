from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend import crud
from backend import models
from backend import schemas
from backend.database import get_db

router = APIRouter(
    # prefix="/usuarios",
    tags=["Usuarios"],
    responses={404: {"description": "No encontrado"}},
)

@router.post("/", response_model=schemas.Usuario) # Ahora esto será realmente /usuarios/
def create_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = crud.get_usuario_by_email(db, email=usuario.email)
    if db_usuario:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    return crud.create_usuario(db=db, usuario=usuario)

@router.get("/", response_model=List[schemas.Usuario]) # Esto será /usuarios/
def read_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    usuarios = crud.get_usuarios(db, skip=skip, limit=limit)
    return usuarios

@router.get("/{usuario_id}", response_model=schemas.Usuario) # Esto será /usuarios/{usuario_id}
def read_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = crud.get_usuario(db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario