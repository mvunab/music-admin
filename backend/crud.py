# Funciones para realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) en la base de datos
from sqlalchemy.orm import Session
from backend import models
from backend import schemas
from passlib.context import CryptContext # Para hashear contraseñas
from datetime import datetime, timezone # Importado para manejar creado_en
import logging

# Suprimir el warning de passlib/bcrypt
logging.getLogger("passlib").setLevel(logging.ERROR)

# Configuración para hashear contraseñas
# Especificar versiones para evitar warnings
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12  # Usar un valor explícito para bcrypt rounds
)

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# CRUD para Usuarios
def get_usuario(db: Session, usuario_id: int):
    return db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()

def get_usuario_by_email(db: Session, email: str):
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()

def get_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Usuario).offset(skip).limit(limit).all()

def create_usuario(db: Session, usuario: schemas.UsuarioCreate):
    hashed_password = get_password_hash(usuario.password)
    # Crear con fecha y hora actuales explícitamente
    db_usuario = models.Usuario(
        email=usuario.email, 
        nombre=usuario.nombre, 
        password_hash=hashed_password,
        creado_en=datetime.now(timezone.utc), # Establecer creado_en explícitamente
        rol_plataforma=usuario.rol_plataforma
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def update_usuario(db: Session, usuario_id: int, usuario_update: schemas.UsuarioBase):
    db_usuario = get_usuario(db, usuario_id)
    if db_usuario:
        # Actualizar campos del usuario
        update_data = usuario_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if key != "password":  # No actualizar password directamente
                setattr(db_usuario, key, value)
        
        db.commit()
        db.refresh(db_usuario)
    return db_usuario

def delete_usuario(db: Session, usuario_id: int):
    db_usuario = get_usuario(db, usuario_id)
    if db_usuario:
        db.delete(db_usuario)
        db.commit()
        return True
    return False

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

# CRUD para Roles Musicales
def get_rol_musical(db: Session, rol_id: int):
    return db.query(models.RolMusical).filter(models.RolMusical.id == rol_id).first()

def get_roles_musicales(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.RolMusical).offset(skip).limit(limit).all()

def create_rol_musical(db: Session, rol: schemas.RolMusicalCreate):
    db_rol = models.RolMusical(**rol.model_dump())
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

# Funciones para gestionar la relación muchos a muchos entre integrantes y roles musicales
def assign_rol_musical_to_integrante(db: Session, integrante_id: int, rol_musical_id: int):
    # Verificar que existe el integrante
    integrante = get_integrante(db, integrante_id=integrante_id)
    if not integrante:
        return None
    
    # Verificar que existe el rol musical
    rol_musical = get_rol_musical(db, rol_id=rol_musical_id)
    if not rol_musical:
        return None
    
    # Verificar si ya existe la asignación para evitar duplicados
    if rol_musical in integrante.roles_musicales:
        return integrante
    
    # Asignar el rol musical al integrante
    integrante.roles_musicales.append(rol_musical)
    db.commit()
    db.refresh(integrante)
    return integrante

def remove_rol_musical_from_integrante(db: Session, integrante_id: int, rol_musical_id: int):
    # Verificar que existe el integrante
    integrante = get_integrante(db, integrante_id=integrante_id)
    if not integrante:
        return None
    
    # Verificar que existe el rol musical
    rol_musical = get_rol_musical(db, rol_id=rol_musical_id)
    if not rol_musical:
        return None
    
    # Verificar si el rol musical está asignado al integrante
    if rol_musical not in integrante.roles_musicales:
        return integrante
    
    # Remover el rol musical del integrante
    integrante.roles_musicales.remove(rol_musical)
    db.commit()
    db.refresh(integrante)
    return integrante
