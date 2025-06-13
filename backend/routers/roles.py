from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud # Cambiado a importación relativa
from .. import schemas # Cambiado a importación relativa
from ..database import get_db # Importamos la función get_db del módulo database

router = APIRouter(
    tags=["Roles"],
    responses={404: {"description": "No encontrado"}},
)

@router.post("/", response_model=schemas.RolMusical)
def create_rol_musical_endpoint(rol: schemas.RolMusicalCreate, db: Session = Depends(get_db)):
    # Aquí podrías añadir lógica para verificar si el rol ya existe por nombre, si es necesario
    return crud.create_rol_musical(db=db, rol=rol)

@router.get("/", response_model=List[schemas.RolMusical])
def read_roles_musicales_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    roles = crud.get_roles_musicales(db, skip=skip, limit=limit)
    return roles

@router.get("/{rol_id}", response_model=schemas.RolMusical)
def read_rol_musical_endpoint(rol_id: int, db: Session = Depends(get_db)):
    db_rol = crud.get_rol_musical(db, rol_id=rol_id)
    if db_rol is None:
        raise HTTPException(status_code=404, detail="Rol musical no encontrado")
    return db_rol

@router.put("/{rol_id}", response_model=schemas.RolMusical)
def update_rol_musical_endpoint(rol_id: int, rol: schemas.RolMusicalCreate, db: Session = Depends(get_db)):
    db_rol = crud.get_rol_musical(db, rol_id=rol_id)
    if db_rol is None:
        raise HTTPException(status_code=404, detail="Rol musical no encontrado")
    
    # Actualizar los atributos del rol
    for key, value in rol.model_dump().items():
        setattr(db_rol, key, value)
    
    db.commit()
    db.refresh(db_rol)
    return db_rol

@router.delete("/{rol_id}", response_model=schemas.RolMusical)
def delete_rol_musical_endpoint(rol_id: int, db: Session = Depends(get_db)):
    db_rol = crud.get_rol_musical(db, rol_id=rol_id)
    if db_rol is None:
        raise HTTPException(status_code=404, detail="Rol musical no encontrado")
    
    db.delete(db_rol)
    db.commit()
    return db_rol
