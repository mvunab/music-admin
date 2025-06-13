from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud
from .. import models
from .. import schemas
from ..database import get_db

router = APIRouter(
    tags=["Asignaciones"],
    responses={404: {"description": "No encontrado"}},
)

@router.post("/", response_model=schemas.Asignacion)
def create_asignacion(asignacion: schemas.AsignacionCreate, db: Session = Depends(get_db)):
    # Verificar que existe el domingo
    domingo = crud.get_domingo(db, domingo_id=asignacion.domingo_id)
    if domingo is None:
        raise HTTPException(status_code=404, detail="Domingo no encontrado")
    
    # Verificar que existe el rol
    rol = crud.get_rol(db, rol_id=asignacion.rol_id)
    if rol is None:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    
    # Verificar que existe el integrante
    integrante = crud.get_integrante(db, integrante_id=asignacion.integrante_id)
    if integrante is None:
        raise HTTPException(status_code=404, detail="Integrante no encontrado")
    
    # Verificar si ya existe una asignación para este domingo y rol
    existing_asignacion = db.query(models.Asignacion).filter(
        models.Asignacion.domingo_id == asignacion.domingo_id,
        models.Asignacion.rol_id == asignacion.rol_id
    ).first()
    
    if existing_asignacion:
        raise HTTPException(status_code=400, detail="Ya existe una asignación para este domingo y rol")
    
    return crud.create_asignacion(db=db, asignacion=asignacion)

@router.get("/", response_model=List[schemas.Asignacion])
def read_asignaciones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    asignaciones = crud.get_asignaciones(db, skip=skip, limit=limit)
    return asignaciones

@router.get("/{asignacion_id}", response_model=schemas.Asignacion)
def read_asignacion(asignacion_id: int, db: Session = Depends(get_db)):
    db_asignacion = crud.get_asignacion(db, asignacion_id=asignacion_id)
    if db_asignacion is None:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")
    return db_asignacion

@router.put("/{asignacion_id}", response_model=schemas.Asignacion)
def update_asignacion(asignacion_id: int, asignacion: schemas.AsignacionCreate, db: Session = Depends(get_db)):
    db_asignacion = crud.get_asignacion(db, asignacion_id=asignacion_id)
    if db_asignacion is None:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")
    
    # Verificar que existe el domingo
    domingo = crud.get_domingo(db, domingo_id=asignacion.domingo_id)
    if domingo is None:
        raise HTTPException(status_code=404, detail="Domingo no encontrado")
    
    # Verificar que existe el rol
    rol = crud.get_rol(db, rol_id=asignacion.rol_id)
    if rol is None:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    
    # Verificar que existe el integrante
    integrante = crud.get_integrante(db, integrante_id=asignacion.integrante_id)
    if integrante is None:
        raise HTTPException(status_code=404, detail="Integrante no encontrado")
    
    # Verificar si ya existe otra asignación para este domingo y rol (que no sea esta misma)
    existing_asignacion = db.query(models.Asignacion).filter(
        models.Asignacion.domingo_id == asignacion.domingo_id,
        models.Asignacion.rol_id == asignacion.rol_id,
        models.Asignacion.id != asignacion_id
    ).first()
    
    if existing_asignacion:
        raise HTTPException(status_code=400, detail="Ya existe otra asignación para este domingo y rol")
    
    # Actualizar los atributos de la asignación
    for key, value in asignacion.model_dump().items():
        setattr(db_asignacion, key, value)
    
    db.commit()
    db.refresh(db_asignacion)
    return db_asignacion

@router.delete("/{asignacion_id}", response_model=schemas.Asignacion)
def delete_asignacion(asignacion_id: int, db: Session = Depends(get_db)):
    db_asignacion = crud.get_asignacion(db, asignacion_id=asignacion_id)
    if db_asignacion is None:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")
    
    db.delete(db_asignacion)
    db.commit()
    return db_asignacion

# Endpoint adicional para obtener asignaciones por domingo
@router.get("/domingo/{domingo_id}", response_model=List[schemas.Asignacion])
def read_asignaciones_by_domingo(domingo_id: int, db: Session = Depends(get_db)):
    # Verificar que existe el domingo
    domingo = crud.get_domingo(db, domingo_id=domingo_id)
    if domingo is None:
        raise HTTPException(status_code=404, detail="Domingo no encontrado")
    
    asignaciones = db.query(models.Asignacion).filter(models.Asignacion.domingo_id == domingo_id).all()
    return asignaciones
