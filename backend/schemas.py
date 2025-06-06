# Definiciones de los esquemas Pydantic para la validación de datos de entrada y salida de la API
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date, datetime

# Esquemas para Usuarios
class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    password: str # La contraseña se enviará en la creación, pero no se devolverá

class Usuario(UsuarioBase):
    id: int
    creado_en: Optional[datetime] = None  # Cambiado para aceptar None

    class Config:
        from_attributes = True # Cambiado de orm_mode

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

# Esquemas para Integrantes
class IntegranteBase(BaseModel):
    nombre: str
    activo: Optional[bool] = True

class IntegranteCreate(IntegranteBase):
    pass

class Integrante(IntegranteBase):
    id: int

    class Config:
        from_attributes = True # Cambiado de orm_mode

# Esquemas para Roles
class RolBase(BaseModel):
    nombre: str

class RolCreate(RolBase):
    pass

class Rol(RolBase):
    id: int

    class Config:
        from_attributes = True # Cambiado de orm_mode

# Esquemas para Pautas
class PautaBase(BaseModel):
    contenido: Optional[str] = None
    tonalidad: Optional[str] = None

class PautaCreate(PautaBase):
    pass

class Pauta(PautaBase):
    id: int

    class Config:
        from_attributes = True # Cambiado de orm_mode

# Esquemas para Domingos
class DomingoBase(BaseModel):
    fecha: date
    ensayo_fecha: Optional[date] = None
    lider_id: Optional[int] = None
    pauta_id: Optional[int] = None

class DomingoCreate(DomingoBase):
    pass

class Domingo(DomingoBase):
    id: int
    # Podríamos incluir aquí los objetos relacionados si quisiéramos devolverlos
    # lider: Optional[Integrante] = None
    # pauta: Optional[Pauta] = None
    # asignaciones: List[Asignacion] = []

    class Config:
        from_attributes = True # Cambiado de orm_mode

# Esquemas para Asignaciones
class AsignacionBase(BaseModel):
    domingo_id: int
    rol_id: int
    integrante_id: int

class AsignacionCreate(AsignacionBase):
    pass

class Asignacion(AsignacionBase):
    id: int
    # Podríamos incluir aquí los objetos relacionados
    # domingo: Domingo
    # rol: Rol
    # integrante: Integrante

    class Config:
        from_attributes = True # Cambiado de orm_mode
