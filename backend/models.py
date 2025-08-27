from sqlalchemy import Boolean, Column, ForeignKey, Text, Date, DateTime, Enum, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func 
from sqlalchemy.dialects import mysql 
import enum

from backend.database import Base 

# Enumeración para roles de usuario en la plataforma
class RolUsuario(enum.Enum):
    admin = "admin"
    regular = "regular"  # Tanto el nombre como el valor en minúsculas para coincidir con la BD

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(mysql.INTEGER(unsigned=True), primary_key=True, index=True) 
    nombre = Column(mysql.VARCHAR(100), nullable=False)
    email = Column(mysql.VARCHAR(150), unique=True, index=True, nullable=False)
    password_hash = Column(mysql.VARCHAR(255), nullable=False)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
    # Rol del usuario en la plataforma (admin o regular)
    rol_plataforma = Column(Enum(RolUsuario), default=RolUsuario.regular)
    # Relación con integrante (un usuario puede ser un integrante de la banda)
    integrante_id = Column(mysql.INTEGER(unsigned=True), ForeignKey("integrantes.id"), nullable=True)
    integrante = relationship("Integrante", back_populates="usuario")

class Integrante(Base):
    __tablename__ = "integrantes"

    id = Column(mysql.INTEGER(unsigned=True), primary_key=True, index=True) 
    nombre = Column(mysql.VARCHAR(100), nullable=False)
    activo = Column(Boolean, default=True)
    # Un integrante puede tener roles permanentes (no asociados a un domingo específico)
    roles_musicales = relationship("RolMusical", secondary="integrantes_roles")
    # Relación con usuario (un integrante está asociado a un usuario)
    usuario = relationship("Usuario", back_populates="integrante", uselist=False)
    # Asignaciones de domingos (roles específicos para cada domingo)
    asignaciones = relationship("Asignacion", back_populates="integrante")

# Tabla para roles musicales (guitarrista, vocalista, etc.)
class RolMusical(Base):
    __tablename__ = "roles_musicales"

    id = Column(mysql.INTEGER(unsigned=True), primary_key=True, index=True) 
    nombre = Column(mysql.VARCHAR(50), unique=True, nullable=False)
    # Integrantes que tienen este rol de forma permanente
    integrantes = relationship("Integrante", secondary="integrantes_roles", overlaps="roles_musicales")
    # Asignaciones para domingos específicos
    asignaciones = relationship("Asignacion", back_populates="rol_musical")

# Tabla intermedia para la relación muchos a muchos entre integrantes y roles musicales
integrantes_roles = Table(
    "integrantes_roles",
    Base.metadata,
    Column("integrante_id", mysql.INTEGER(unsigned=True), ForeignKey("integrantes.id"), primary_key=True),
    Column("rol_musical_id", mysql.INTEGER(unsigned=True), ForeignKey("roles_musicales.id"), primary_key=True)
)

class Pauta(Base):
    __tablename__ = "pautas"

    id = Column(mysql.INTEGER(unsigned=True), primary_key=True, index=True) 
    contenido = Column(Text)
    tonalidad = Column(mysql.VARCHAR(20))
    
    # Relaciones
    domingos = relationship("Domingo", back_populates="pauta")

class Domingo(Base):
    __tablename__ = "domingos"

    id = Column(mysql.INTEGER(unsigned=True), primary_key=True, index=True) 
    fecha = Column(Date, unique=True, nullable=False)
    ensayo_fecha = Column(Date, nullable=True)
    lider_id = Column(mysql.INTEGER(unsigned=True), ForeignKey("integrantes.id")) 
    pauta_id = Column(mysql.INTEGER(unsigned=True), ForeignKey("pautas.id"))
    
    # Relaciones
    lider = relationship("Integrante", foreign_keys=[lider_id])
    pauta = relationship("Pauta", back_populates="domingos")
    asignaciones = relationship("Asignacion", back_populates="domingo")

class Asignacion(Base):
    __tablename__ = "asignaciones"

    id = Column(mysql.INTEGER(unsigned=True), primary_key=True, index=True)
    domingo_id = Column(mysql.INTEGER(unsigned=True), ForeignKey("domingos.id"))
    rol_musical_id = Column(mysql.INTEGER(unsigned=True), ForeignKey("roles_musicales.id"))
    integrante_id = Column(mysql.INTEGER(unsigned=True), ForeignKey("integrantes.id"))
    
    # Relaciones
    domingo = relationship("Domingo", back_populates="asignaciones")
    rol_musical = relationship("RolMusical", back_populates="asignaciones")
    integrante = relationship("Integrante", back_populates="asignaciones") 
    
