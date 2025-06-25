# Definiciones de los esquemas Pydantic para la validación de datos de entrada y salida de la API
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Any
from datetime import date, datetime
from enum import Enum

# Enumeración para roles de usuario en la plataforma
class RolUsuarioEnum(str, Enum):
    admin = "admin"
    regular = "regular"  # Tanto el nombre como el valor en minúsculas para coincidir con la BD

# Esquema para el login
class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str

# Esquema para el token (respuesta del login)
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Esquemas simples para definiciones básicas
class RolMusicalBase(BaseModel):
    nombre: str

class RolMusicalCreate(RolMusicalBase):
    pass

class RolMusicalSimple(RolMusicalBase):
    id: int

    class Config:
        from_attributes = True

class IntegranteBase(BaseModel):
    nombre: str
    activo: Optional[bool] = True

class IntegranteCreate(IntegranteBase):
    pass

class IntegranteSimple(IntegranteBase):
    id: int

    class Config:
        from_attributes = True

class PautaBase(BaseModel):
    contenido: Optional[str] = None
    tonalidad: Optional[str] = None

class PautaCreate(PautaBase):
    pass

class PautaSimple(PautaBase):
    id: int

    class Config:
        from_attributes = True

class DomingoBase(BaseModel):
    fecha: date
    ensayo_fecha: Optional[date] = None
    lider_id: Optional[int] = None
    pauta_id: Optional[int] = None

class DomingoCreate(DomingoBase):
    pass

class DomingoSimple(DomingoBase):
    id: int

    class Config:
        from_attributes = True

class AsignacionBase(BaseModel):
    domingo_id: int
    rol_musical_id: int
    integrante_id: int

class AsignacionCreate(AsignacionBase):
    pass

class AsignacionSimple(AsignacionBase):
    id: int

    class Config:
        from_attributes = True

# Esquemas para Usuarios
class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr
    rol_plataforma: Optional[RolUsuarioEnum] = RolUsuarioEnum.regular
    integrante_id: Optional[int] = None
    is_admin: Optional[bool] = False

class UsuarioCreate(UsuarioBase):
    password: str # La contraseña se enviará en la creación, pero no se devolverá

class Usuario(UsuarioBase):
    id: int
    creado_en: Optional[datetime] = None

    class Config:
        from_attributes = True

# Esquemas detallados con relaciones
class RolMusical(RolMusicalSimple):
    integrantes: List[IntegranteSimple] = []
    asignaciones: List["AsignacionSimple"] = []

    class Config:
        from_attributes = True

class Integrante(IntegranteSimple):
    roles_musicales: List[RolMusicalSimple] = []
    asignaciones: List["AsignacionSimple"] = []
    usuario: Optional["UsuarioSimple"] = None

    class Config:
        from_attributes = True

class UsuarioSimple(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    rol_plataforma: RolUsuarioEnum
    is_admin: bool = False

    class Config:
        from_attributes = True

class UsuarioDetalle(Usuario):
    integrante: Optional[IntegranteSimple] = None

    class Config:
        from_attributes = True

class Pauta(PautaSimple):
    domingos: List["DomingoSimple"] = []

    class Config:
        from_attributes = True

class DomingoDetalle(DomingoSimple):
    lider: Optional[IntegranteSimple] = None
    pauta: Optional[PautaSimple] = None
    asignaciones: List["AsignacionSimple"] = []

    class Config:
        from_attributes = True

class AsignacionDetalle(AsignacionSimple):
    domingo: Optional[DomingoSimple] = None
    rol_musical: Optional[RolMusicalSimple] = None
    integrante: Optional[IntegranteSimple] = None

    class Config:
        from_attributes = True

# Para resolver referencias circulares
from typing import ForwardRef
Integrante.update_forward_refs()
RolMusical.update_forward_refs()
Pauta.update_forward_refs()
DomingoDetalle.update_forward_refs()
AsignacionDetalle.update_forward_refs()
