# Definiciones de los modelos SQLAlchemy que se mapean a las tablas de schema.sql
from sqlalchemy import Boolean, Column, ForeignKey, Text, Date, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func # Para CURRENT_TIMESTAMP
from sqlalchemy.dialects import mysql # Importar el dialecto de MySQL

from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(mysql.INTEGER(unsigned=True), primary_key=True, index=True) # Cambiado a UNSIGNED
    nombre = Column(mysql.VARCHAR(100), nullable=False)
    email = Column(mysql.VARCHAR(150), unique=True, index=True, nullable=False)
    password_hash = Column(mysql.VARCHAR(255), nullable=False)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())

class Integrante(Base):
    __tablename__ = "integrantes"

    id = Column(mysql.INTEGER(unsigned=True), primary_key=True, index=True) # Cambiado a UNSIGNED
    nombre = Column(mysql.VARCHAR(100), nullable=False)
    activo = Column(Boolean, default=True)

class Rol(Base):
    __tablename__ = "roles"

    id = Column(mysql.INTEGER(unsigned=True), primary_key=True, index=True) # Cambiado a UNSIGNED
    nombre = Column(mysql.VARCHAR(50), unique=True, nullable=False)

class Pauta(Base):
    __tablename__ = "pautas"

    id = Column(mysql.INTEGER(unsigned=True), primary_key=True, index=True) # Cambiado a UNSIGNED
    contenido = Column(Text)
    tonalidad = Column(mysql.VARCHAR(20))

class Domingo(Base):
    __tablename__ = "domingos"

    id = Column(mysql.INTEGER(unsigned=True), primary_key=True, index=True) # Cambiado a UNSIGNED
    fecha = Column(Date, unique=True, nullable=False)
    ensayo_fecha = Column(Date, nullable=True)
    lider_id = Column(mysql.INTEGER(unsigned=True), ForeignKey("integrantes.id")) # Cambiado a UNSIGNED. Dejar esta FK por ahora.
    pauta_id = Column(mysql.INTEGER(unsigned=True), ForeignKey("pautas.id")) # Cambiado a UNSIGNED. Dejar esta FK por ahora.

class Asignacion(Base):
    __tablename__ = "asignaciones"

    id = Column(mysql.INTEGER(unsigned=True), primary_key=True, index=True)
    domingo_id = Column(mysql.INTEGER(unsigned=True)) # FK a domingos.id comentada temporalmente
    rol_id = Column(mysql.INTEGER(unsigned=True)) # FK a roles.id comentada temporalmente
    integrante_id = Column(mysql.INTEGER(unsigned=True)) # FK a integrantes.id comentada temporalmente
    # domingo_id = Column(mysql.INTEGER(unsigned=True), ForeignKey("domingos.id", ondelete="CASCADE"))
    # rol_id = Column(mysql.INTEGER(unsigned=True), ForeignKey("roles.id"))
    # integrante_id = Column(mysql.INTEGER(unsigned=True), ForeignKey("integrantes.id"))
