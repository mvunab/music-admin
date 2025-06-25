from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend import crud
from backend import models
from backend import schemas
from backend.database import get_db
from backend.routers.auth import get_current_user

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

@router.put("/{usuario_id}", response_model=schemas.Usuario)
def update_usuario(
    usuario_id: int, 
    usuario_update: schemas.UsuarioBase, 
    db: Session = Depends(get_db),
    current_user: schemas.Usuario = Depends(get_current_user)
):
    # Verificar si el usuario actual es administrador
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren privilegios de administrador para esta operación"
        )
    
    # Verificar si el usuario a actualizar existe
    db_usuario = crud.get_usuario(db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Actualizar el usuario
    updated_usuario = crud.update_usuario(db=db, usuario_id=usuario_id, usuario_update=usuario_update)
    return updated_usuario

@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_usuario(
    usuario_id: int, 
    db: Session = Depends(get_db),
    current_user: schemas.Usuario = Depends(get_current_user)
):
    # Verificar si el usuario actual es administrador
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren privilegios de administrador para esta operación"
        )
    
    # Verificar si el usuario a eliminar existe
    db_usuario = crud.get_usuario(db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # No permitir eliminar al propio usuario
    if db_usuario.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes eliminar tu propio usuario"
        )
    
    # Eliminar el usuario
    result = crud.delete_usuario(db=db, usuario_id=usuario_id)
    
    # Si por alguna razón no se pudo eliminar
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo eliminar el usuario"
        )