from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth import router as auth_router
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

app = FastAPI(title="ConsultaPlaca API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

app.include_router(auth_router)

@app.get("/health")
def health():
    return {"status": "ok", "proyecto": "ConsultaPlaca"}

@app.get("/db-test")
def db_test():
    res = supabase.table("usuarios").select("*").execute()
    return {"db": "conectada", "usuarios": len(res.data)}

@app.get("/consulta/{placa}")
def consultar(placa: str):
    import re
    placa = placa.upper().strip()
    if not re.match(r'^[A-Z]{3}-?\d{3}$', placa):
        return {"error": "Placa inválida. Ejemplo: ABC123"}
    return {"placa": placa, "mensaje": "Endpoint listo"}