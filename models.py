# Definiciones de los modelos SQLAlchemy que se mapean a las tablas de schema.sql
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func # Para CURRENT_TIMESTAMP

from .database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())

class Integrante(Base):
    __tablename__ = "integrantes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    activo = Column(Boolean, default=True)

    # Relaciones inversas (opcional, pero útil para acceder desde el integrante)
    # asignaciones = relationship("Asignacion", back_populates="integrante")
    # domingos_liderados = relationship("Domingo", back_populates="lider")

class Rol(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)

    # Relaciones inversas
    # asignaciones = relationship("Asignacion", back_populates="rol")

class Pauta(Base):
    __tablename__ = "pautas"

    id = Column(Integer, primary_key=True, index=True)
    contenido = Column(Text)
    tonalidad = Column(String(20))

    # Relaciones inversas
    # domingos = relationship("Domingo", back_populates="pauta")

class Domingo(Base):
    __tablename__ = "domingos"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, unique=True, nullable=False)
    ensayo_fecha = Column(Date, nullable=True)
    lider_id = Column(Integer, ForeignKey("integrantes.id"))
    pauta_id = Column(Integer, ForeignKey("pautas.id"))

    # Relaciones (muchos a uno)
    # lider = relationship("Integrante", back_populates="domingos_liderados")
    # pauta = relationship("Pauta", back_populates="domingos")

    # Relaciones inversas (uno a muchos)
    # asignaciones = relationship("Asignacion", back_populates="domingo")

class Asignacion(Base):
    __tablename__ = "asignaciones"

    id = Column(Integer, primary_key=True, index=True)
    domingo_id = Column(Integer, ForeignKey("domingos.id", ondelete="CASCADE"))
    rol_id = Column(Integer, ForeignKey("roles.id"))
    integrante_id = Column(Integer, ForeignKey("integrantes.id"))

    # Relaciones (muchos a uno)
    # domingo = relationship("Domingo", back_populates="asignaciones")
    # rol = relationship("Rol", back_populates="asignaciones")
    # integrante = relationship("Integrante", back_populates="asignaciones")

    # Constraints (ejemplo, UNIQUE(domingo_id, rol_id) se maneja a nivel de DB o con validaciones)
