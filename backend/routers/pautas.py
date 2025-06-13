from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend import crud
from backend import schemas
from backend.database import get_db

router = APIRouter(
    tags=["Pautas"],
    responses={404: {"description": "No encontrado"}},
)

@router.post("/", response_model=schemas.Pauta)
def create_pauta(pauta: schemas.PautaCreate, db: Session = Depends(get_db)):
    return crud.create_pauta(db=db, pauta=pauta)

@router.get("/", response_model=List[schemas.Pauta])
def read_pautas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pautas = crud.get_pautas(db, skip=skip, limit=limit)
    return pautas

@router.get("/{pauta_id}", response_model=schemas.Pauta)
def read_pauta(pauta_id: int, db: Session = Depends(get_db)):
    db_pauta = crud.get_pauta(db, pauta_id=pauta_id)
    if db_pauta is None:
        raise HTTPException(status_code=404, detail="Pauta no encontrada")
    return db_pauta

@router.put("/{pauta_id}", response_model=schemas.Pauta)
def update_pauta(pauta_id: int, pauta: schemas.PautaCreate, db: Session = Depends(get_db)):
    db_pauta = crud.get_pauta(db, pauta_id=pauta_id)
    if db_pauta is None:
        raise HTTPException(status_code=404, detail="Pauta no encontrada")
    
    # Actualizar los atributos de la pauta
    for key, value in pauta.model_dump().items():
        setattr(db_pauta, key, value)
    
    db.commit()
    db.refresh(db_pauta)
    return db_pauta

@router.delete("/{pauta_id}", response_model=schemas.Pauta)
def delete_pauta(pauta_id: int, db: Session = Depends(get_db)):
    db_pauta = crud.get_pauta(db, pauta_id=pauta_id)
    if db_pauta is None:
        raise HTTPException(status_code=404, detail="Pauta no encontrada")
    
    db.delete(db_pauta)
    db.commit()
    return db_pauta
