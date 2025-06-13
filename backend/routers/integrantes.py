from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend import crud
from backend import schemas
from backend.database import get_db

router = APIRouter(
    tags=["Integrantes"],
    responses={404: {"description": "No encontrado"}},
)

@router.post("/", response_model=schemas.Integrante)
def create_integrante(integrante: schemas.IntegranteCreate, db: Session = Depends(get_db)):
    return crud.create_integrante(db=db, integrante=integrante)

@router.get("/", response_model=List[schemas.Integrante])
def read_integrantes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    integrantes = crud.get_integrantes(db, skip=skip, limit=limit)
    return integrantes

@router.get("/{integrante_id}", response_model=schemas.Integrante)
def read_integrante(integrante_id: int, db: Session = Depends(get_db)):
    db_integrante = crud.get_integrante(db, integrante_id=integrante_id)
    if db_integrante is None:
        raise HTTPException(status_code=404, detail="Integrante no encontrado")
    return db_integrante

@router.put("/{integrante_id}", response_model=schemas.Integrante)
def update_integrante(integrante_id: int, integrante: schemas.IntegranteCreate, db: Session = Depends(get_db)):
    db_integrante = crud.get_integrante(db, integrante_id=integrante_id)
    if db_integrante is None:
        raise HTTPException(status_code=404, detail="Integrante no encontrado")
    
    # Actualizar los atributos del integrante
    for key, value in integrante.model_dump().items():
        setattr(db_integrante, key, value)
    
    db.commit()
    db.refresh(db_integrante)
    return db_integrante

@router.delete("/{integrante_id}", response_model=schemas.Integrante)
def delete_integrante(integrante_id: int, db: Session = Depends(get_db)):
    db_integrante = crud.get_integrante(db, integrante_id=integrante_id)
    if db_integrante is None:
        raise HTTPException(status_code=404, detail="Integrante no encontrado")
    
    db.delete(db_integrante)
    db.commit()
    return db_integrante

# Nuevos endpoints para gestionar roles musicales de un integrante
@router.post("/{integrante_id}/roles/{rol_musical_id}", response_model=schemas.Integrante)
def assign_rol_to_integrante(integrante_id: int, rol_musical_id: int, db: Session = Depends(get_db)):
    db_integrante = crud.assign_rol_musical_to_integrante(db, integrante_id, rol_musical_id)
    if db_integrante is None:
        raise HTTPException(
            status_code=404, 
            detail="Integrante o rol musical no encontrado"
        )
    return db_integrante

@router.delete("/{integrante_id}/roles/{rol_musical_id}", response_model=schemas.Integrante)
def remove_rol_from_integrante(integrante_id: int, rol_musical_id: int, db: Session = Depends(get_db)):
    db_integrante = crud.remove_rol_musical_from_integrante(db, integrante_id, rol_musical_id)
    if db_integrante is None:
        raise HTTPException(
            status_code=404, 
            detail="Integrante o rol musical no encontrado"
        )
    return db_integrante
