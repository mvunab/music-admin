
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import crud
import schemas
from database import SessionLocal

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Rol)
def create_rol_endpoint(rol: schemas.RolCreate, db: Session = Depends(get_db)):
    # Aquí podrías añadir lógica para verificar si el rol ya existe por nombre, si es necesario
    return crud.create_rol(db=db, rol=rol)

@router.get("/", response_model=List[schemas.Rol])
def read_roles_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    roles = crud.get_roles(db, skip=skip, limit=limit)
    return roles

@router.get("/{rol_id}", response_model=schemas.Rol)
def read_rol_endpoint(rol_id: int, db: Session = Depends(get_db)):
    db_rol = crud.get_rol(db, rol_id=rol_id)
    if db_rol is None:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return db_rol

# Aquí podrías añadir endpoints para actualizar (PUT) y eliminar (DELETE) roles si es necesario en el futuro.
# Ejemplo de endpoint PUT (actualizar):
# @router.put("/{rol_id}", response_model=schemas.Rol)
# def update_rol_endpoint(rol_id: int, rol_update: schemas.RolUpdate, db: Session = Depends(get_db)):
#     db_rol = crud.get_rol(db, rol_id=rol_id)
#     if db_rol is None:
#         raise HTTPException(status_code=404, detail="Rol no encontrado")
#     # Asumiendo que tienes una función crud.update_rol y un schema schemas.RolUpdate
#     # return crud.update_rol(db=db, rol_id=rol_id, rol_update=rol_update)
#     raise HTTPException(status_code=501, detail="Actualización de rol no implementada")

# Ejemplo de endpoint DELETE (eliminar):
# @router.delete("/{rol_id}", response_model=schemas.Rol) # O algún schema de confirmación
# def delete_rol_endpoint(rol_id: int, db: Session = Depends(get_db)):
#     db_rol = crud.get_rol(db, rol_id=rol_id)
#     if db_rol is None:
#         raise HTTPException(status_code=404, detail="Rol no encontrado")
#     # Asumiendo que tienes una función crud.delete_rol
#     # crud.delete_rol(db=db, rol_id=rol_id)
#     # return {"ok": True, "detail": "Rol eliminado"} # O el objeto eliminado
#     raise HTTPException(status_code=501, detail="Eliminación de rol no implementada")
