# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import nutry, maps, match # Importa todos os módulos
from app.services.data_service import DataService # Para carregar os dados no startup

app = FastAPI(title="SaveNutri API")

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Rotas de IA (Nutrição)
app.include_router(nutry.router, prefix="/ai", tags=["Nutrition"])

# 2. Rotas de Mapas (GeoJSON)
app.include_router(maps.router, prefix="/geojson", tags=["Maps"])

# 3. Rotas de Inteligência de Match
app.include_router(match.router, prefix="/match", tags=["Matchmaking"])

# Evento de Inicialização (Carrega o GeoJSON de Teresópolis)
@app.on_event("startup")
async def startup_event():
    # Aqui chamamos o serviço responsável por carregar os dados iniciais
    data_service = DataService()
    await data_service.load_initial_data()

@app.get("/")
async def root():
    return {"message": "SaveNutri API is running!"}