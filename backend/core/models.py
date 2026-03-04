from sqlalchemy import Column, Integer, String, Boolean, Numeric, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class Producto(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    precio = Column(Numeric(10, 2))
    iva = Column(Integer)
    categoria = Column(String)
    icono = Column(String)
    activo = Column(Boolean, default=True)

class Sesion(Base):
    __tablename__ = "sesiones"
    id = Column(Integer, primary_key=True, index=True)
    usuario = Column(String)
    apertura = Column(DateTime, default=datetime.utcnow)
    cierre = Column(DateTime, nullable=True)
    efectivo_inicial = Column(Numeric(10, 2))
    efectivo_final = Column(Numeric(10, 2), nullable=True)
    estado = Column(String)

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String, unique=True, index=True)
    sesion_id = Column(Integer, ForeignKey("sesiones.id"))
    fecha = Column(DateTime, default=datetime.utcnow)
    lineas = Column(JSON)
    subtotal = Column(Numeric(10, 2))
    iva = Column(Numeric(10, 2))
    total = Column(Numeric(10, 2))
    tipo = Column(String)
    estado = Column(String)
    sesion = relationship("Sesion")
    registro = relationship("RegistroVERIFACTU", back_populates="ticket", uselist=False)

class RegistroVERIFACTU(Base):
    __tablename__ = "registros_verifactu"
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), unique=True)
    hash_anterior = Column(String)
    hash_actual = Column(String)
    xml_registro = Column(String)
    firma_xades = Column(String)
    qr_data = Column(String)
    csv_aeat = Column(String, nullable=True)
    fecha_envio = Column(DateTime, nullable=True)
    estado_envio = Column(String)

    ticket = relationship("Ticket", back_populates="registro")

class Mesa(Base):
    __tablename__ = "mesas"
    id = Column(Integer, primary_key=True, index=True)
    numero = Column(Integer, unique=True)
    zona = Column(String)
    ocupada = Column(Boolean, default=False)
    comanda_actual = Column(JSON, nullable=True)
