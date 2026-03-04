from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from core.models import Producto
from pydantic import BaseModel
from decimal import Decimal
from typing import List

router = APIRouter()

class ProductoCreate(BaseModel):
    nombre: str
    precio: Decimal
    iva: int
    categoria: str
    icono: str

class ProductoResponse(ProductoCreate):
    id: int
    activo: bool

    class Config:
        orm_mode = True

@router.get("/", response_model=List[ProductoResponse])
def listar_productos(db: Session = Depends(get_db)):
    return db.query(Producto).filter(Producto.activo == True).all()

@router.post("/", response_model=ProductoResponse)
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    db_producto = Producto(**producto.dict())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

@router.put("/{id}", response_model=ProductoResponse)
def actualizar_producto(id: int, producto: ProductoCreate, db: Session = Depends(get_db)):
    db_producto = db.query(Producto).filter(Producto.id == id).first()
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    for key, value in producto.dict().items():
        setattr(db_producto, key, value)
    db.commit()
    db.refresh(db_producto)
    return db_producto

@router.delete("/{id}")
def eliminar_producto(id: int, db: Session = Depends(get_db)):
    db_producto = db.query(Producto).filter(Producto.id == id).first()
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db_producto.activo = False
    db.commit()
    return {"message": "Producto eliminado"}
