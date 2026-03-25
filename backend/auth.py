from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import bcrypt
from jose import jwt
from datetime import datetime, timedelta
import os
from supabase import create_client

# Conexión a Supabase
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

# Clave secreta para firmar los tokens JWT
# En producción esto va en el .env, por ahora está aquí
SECRET_KEY = "consultaplaca-secret-2024"

router = APIRouter()

# Modelos: definen qué datos esperamos recibir
class RegistroData(BaseModel):
    email: str
    password: str

class LoginData(BaseModel):
    email: str
    password: str


@router.post("/auth/register")
def registrar(datos: RegistroData):
    # 1. Verificar que el email no exista ya
    existente = supabase.table("usuarios")\
        .select("id")\
        .eq("email", datos.email)\
        .execute()

    if existente.data:
        raise HTTPException(status_code=400, detail="Ese email ya está registrado")

    # 2. Hashear la contraseña (nunca guardar en texto plano)
    password_hash = bcrypt.hashpw(
        datos.password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    # 3. Guardar el usuario en Supabase con 1 crédito gratis
    nuevo = supabase.table("usuarios").insert({
        "email": datos.email,
        "password_hash": password_hash,
        "creditos": 1
    }).execute()

    return {"mensaje": "Cuenta creada exitosamente", "email": datos.email}


@router.post("/auth/login")
def login(datos: LoginData):
    # 1. Buscar el usuario por email
    resultado = supabase.table("usuarios")\
        .select("*")\
        .eq("email", datos.email)\
        .execute()

    if not resultado.data:
        raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")

    usuario = resultado.data[0]

    # 2. Verificar la contraseña contra el hash guardado
    password_correcta = bcrypt.checkpw(
        datos.password.encode("utf-8"),
        usuario["password_hash"].encode("utf-8")
    )

    if not password_correcta:
        raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")

    # 3. Generar el token JWT con 7 días de validez
    token = jwt.encode({
        "sub": usuario["id"],
        "email": usuario["email"],
        "exp": datetime.utcnow() + timedelta(days=7)
    }, SECRET_KEY, algorithm="HS256")

    return {
        "token": token,
        "email": usuario["email"],
        "creditos": usuario["creditos"]
    }