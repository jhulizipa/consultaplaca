from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv() # carga el archivo .env

app = FastAPI(title="ConsultaPlaca API")

app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:5173"],
  allow_methods=["*"],
  allow_headers=["*"],
)

@app.get("/health")
def health():
  return {"status": "ok", "proyecto": "ConsultaPlaca"}

@app.get("/consulta/{placa}")
def consultar(placa: str):
  import re
  placa = placa.upper().strip()
  if not re.match(r'^[A-Z]{3}-?\d{3}$', placa):
    return {"error": "Placa inválida. Ejemplo: ABC123"}
  return {"placa": placa, "mensaje": "Endpoint listo"}