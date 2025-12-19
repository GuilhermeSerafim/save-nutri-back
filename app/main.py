# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import nutry # Importa suas novas rotas

app = FastAPI(title="SaveNutri API")

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas do módulo de nutrição
app.include_router(nutry.router, prefix="/ai", tags=["Nutrition"])

@app.get("/")
async def root():
    return {"message": "SaveNutri API is running!"}