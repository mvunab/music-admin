from sqlalchemy import Boolean, Column, ForeignKey, Text, Date, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func 
from sqlalchemy.dialects import mysql 

from .database import Base 

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(mysql.INTEGER(unsigned=True), primary_key=True, index=True) 
    nombre = Column(mysql.VARCHAR(100), nullable=False)
    email = Column(mysql.VARCHAR(150), unique=True, index=True, nullable=False)
    password_hash = Column(mysql.VARCHAR(255), nullable=False)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())

class Integrante(Base):
    __tablename__ = "integrantes"

    id = Column(mysql.INTEGER(unsigned=True), primary_key=True, index=True) 
    nombre = Column(mysql.VARCHAR(100), nullable=False)
    activo = Column(Boolean, default=True)

class Rol(Base):
    __tablename__ = "roles"

    id = Column(mysql.INTEGER(unsigned=True), primary_key=True, index=True) 
    nombre = Column(mysql.VARCHAR(50), unique=True, nullable=False)

class Pauta(Base):
    __tablename__ = "pautas"

    id = Column(mysql.INTEGER(unsigned=True), primary_key=True, index=True) 
    contenido = Column(Text)
    tonalidad = Column(mysql.VARCHAR(20))

class Domingo(Base):
    __tablename__ = "domingos"

    id = Column(mysql.INTEGER(unsigned=True), primary_key=True, index=True) 
    fecha = Column(Date, unique=True, nullable=False)
    ensayo_fecha = Column(Date, nullable=True)
    lider_id = Column(mysql.INTEGER(unsigned=True), ForeignKey("integrantes.id")) 
    pauta_id = Column(mysql.INTEGER(unsigned=True), ForeignKey("pautas.id")) 

class Asignacion(Base):
    __tablename__ = "asignaciones"

    id = Column(mysql.INTEGER(unsigned=True), primary_key=True, index=True)
    domingo_id = Column(mysql.INTEGER(unsigned=True)) 
    rol_id = Column(mysql.INTEGER(unsigned=True)) 
    integrante_id = Column(mysql.INTEGER(unsigned=True)) 
    
