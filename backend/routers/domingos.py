from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from .. import crud
from .. import models
from .. import schemas
from ..database import get_db

router = APIRouter(
    tags=["Domingos"],
    responses={404: {"description": "No encontrado"}},
)

@router.post("/", response_model=schemas.Domingo)
def create_domingo(domingo: schemas.DomingoCreate, db: Session = Depends(get_db)):
    return crud.create_domingo(db=db, domingo=domingo)

@router.get("/", response_model=List[schemas.Domingo])
def read_domingos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    domingos = crud.get_domingos(db, skip=skip, limit=limit)
    return domingos

@router.get("/{domingo_id}", response_model=schemas.Domingo)
def read_domingo(domingo_id: int, db: Session = Depends(get_db)):
    db_domingo = crud.get_domingo(db, domingo_id=domingo_id)
    if db_domingo is None:
        raise HTTPException(status_code=404, detail="Domingo no encontrado")
    return db_domingo

@router.put("/{domingo_id}", response_model=schemas.Domingo)
def update_domingo(domingo_id: int, domingo: schemas.DomingoCreate, db: Session = Depends(get_db)):
    db_domingo = crud.get_domingo(db, domingo_id=domingo_id)
    if db_domingo is None:
        raise HTTPException(status_code=404, detail="Domingo no encontrado")
    
    # Actualizar los atributos del domingo
    for key, value in domingo.model_dump().items():
        setattr(db_domingo, key, value)
    
    db.commit()
    db.refresh(db_domingo)
    return db_domingo

@router.delete("/{domingo_id}", response_model=schemas.Domingo)
def delete_domingo(domingo_id: int, db: Session = Depends(get_db)):
    db_domingo = crud.get_domingo(db, domingo_id=domingo_id)
    if db_domingo is None:
        raise HTTPException(status_code=404, detail="Domingo no encontrado")
    
    db.delete(db_domingo)
    db.commit()
    return db_domingo

# Endpoint adicional para obtener los domingos por fecha
@router.get("/fecha/{fecha}", response_model=schemas.Domingo)
def read_domingo_by_fecha(fecha: date, db: Session = Depends(get_db)):
    db_domingo = db.query(models.Domingo).filter(models.Domingo.fecha == fecha).first()
    if db_domingo is None:
        raise HTTPException(status_code=404, detail="Domingo no encontrado para esta fecha")
    return db_domingo
