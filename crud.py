# Funciones para realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) en la base de datos
from sqlalchemy.orm import Session
import models  # Cambiado de from . import models
import schemas # Cambiado de from . import schemas
from passlib.context import CryptContext # Para hashear contraseñas

# Configuración para hashear contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

# CRUD para Usuarios
def get_usuario(db: Session, usuario_id: int):
    return db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()

def get_usuario_by_email(db: Session, email: str):
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()

def get_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Usuario).offset(skip).limit(limit).all()

def create_usuario(db: Session, usuario: schemas.UsuarioCreate):
    hashed_password = get_password_hash(usuario.password)
    db_usuario = models.Usuario(email=usuario.email, nombre=usuario.nombre, password_hash=hashed_password)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

# CRUD para Integrantes
def get_integrante(db: Session, integrante_id: int):
    return db.query(models.Integrante).filter(models.Integrante.id == integrante_id).first()

def get_integrantes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Integrante).offset(skip).limit(limit).all()

def create_integrante(db: Session, integrante: schemas.IntegranteCreate):
    db_integrante = models.Integrante(**integrante.model_dump())
    db.add(db_integrante)
    db.commit()
    db.refresh(db_integrante)
    return db_integrante

# CRUD para Roles
def get_rol(db: Session, rol_id: int):
    return db.query(models.Rol).filter(models.Rol.id == rol_id).first()

def get_roles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Rol).offset(skip).limit(limit).all()

def create_rol(db: Session, rol: schemas.RolCreate):
    db_rol = models.Rol(**rol.model_dump())
    db.add(db_rol)
    db.commit()
    db.refresh(db_rol)
    return db_rol

# CRUD para Pautas
def get_pauta(db: Session, pauta_id: int):
    return db.query(models.Pauta).filter(models.Pauta.id == pauta_id).first()

def get_pautas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Pauta).offset(skip).limit(limit).all()

def create_pauta(db: Session, pauta: schemas.PautaCreate):
    db_pauta = models.Pauta(**pauta.model_dump())
    db.add(db_pauta)
    db.commit()
    db.refresh(db_pauta)
    return db_pauta

# CRUD para Domingos
def get_domingo(db: Session, domingo_id: int):
    return db.query(models.Domingo).filter(models.Domingo.id == domingo_id).first()

def get_domingos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Domingo).offset(skip).limit(limit).all()

def create_domingo(db: Session, domingo: schemas.DomingoCreate):
    db_domingo = models.Domingo(**domingo.model_dump())
    db.add(db_domingo)
    db.commit()
    db.refresh(db_domingo)
    return db_domingo

# CRUD para Asignaciones
def get_asignacion(db: Session, asignacion_id: int):
    return db.query(models.Asignacion).filter(models.Asignacion.id == asignacion_id).first()

def get_asignaciones(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Asignacion).offset(skip).limit(limit).all()

def create_asignacion(db: Session, asignacion: schemas.AsignacionCreate):
    db_asignacion = models.Asignacion(**asignacion.model_dump())
    db.add(db_asignacion)
    db.commit()
    db.refresh(db_asignacion)
    return db_asignacion
