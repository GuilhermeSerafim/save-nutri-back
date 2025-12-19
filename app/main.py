# Imports da biblioteca padrão do Python
import os
import json
import random

# Imports de terceiros (instale-os via pip)
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from geopy.distance import geodesic
from openai import OpenAI
from pydantic import BaseModel
from app.core.config import settings

# Carrega as variáveis do arquivo .env
load_dotenv()

app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CONFIGURAÇÃO DA IA ---
# ⚠️ IMPORTANTE: Gere uma chave nova na OpenAI, a que você postou pode ter sido comprometida.
OPENAI_API_KEY = "" # <--- COLE SUA CHAVE NOVA AQUI
client = OpenAI(api_key=settings.OPENAI_API_KEY)

# --- BANCO DE DADOS EM MEMÓRIA ---
DB = {
    "features": []
}

# --- MODELOS DE DADOS ---
class MenuRequest(BaseModel):
    products: list[str]
    school_demand: str = "Hortifruti"

# --- ROTA DE IA (Gera Cardápio) ---
@app.post("/ai/generate_menu")
def generate_real_ai_menu(request: MenuRequest):
    print(f"🤖 IA (GPT) Recebeu ingredientes: {request.products}")
    
    ingredientes_texto = ", ".join(request.products)
    
    prompt = f"""
    Você é uma Nutricionista especialista no PNAE.
    
    CONTEXTO:
    Agricultor tem: {ingredientes_texto}.
    Crie cardápio para Segunda e Terça.
    
    RESPOSTA (JSON PURO):
    {{
        "menu_suggestion": {{
            "segunda": {{ "prato": "...", "ingredientes_usados": [...], "analise_ia": "..." }},
            "terca": {{ "prato": "...", "ingredientes_usados": [...], "analise_ia": "..." }}
        }}
    }}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente JSON útil."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        return json.loads(content)

    except Exception as e:
        print(f"❌ Erro na OpenAI: {e}")
        # Fallback de segurança
        return {
            "menu_suggestion": {
                "segunda": {
                    "prato": "Salada da Agricultura Familiar",
                    "ingredientes_usados": request.products[:3],
                    "analise_ia": "Sugestão offline (Erro na IA)."
                },
                "terca": {
                    "prato": "Sopa de Legumes Locais",
                    "ingredientes_usados": request.products,
                    "analise_ia": "Opção nutritiva de emergência."
                }
            }
        }

# --- INICIALIZAÇÃO (CARREGA DADOS) ---
@app.on_event("startup")
async def load_data():
    try:
        with open("data/TeresopolisEscolasELocaisDeProducao.geojson", "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            
        processed_features = []
        PRODUTOS_SAFRA = ["Alface", "Couve", "Tomate", "Cenoura", "Beterraba", "Inhame", "Brócolis", "Caqui"]
        DEMANDAS_ESCOLA = ["Hortifruti Variado", "Legumes", "Frutas da Estação", "Folhosas"]
        
        # Loop corrigido com ID único sequencial
        for i, feature in enumerate(raw_data['features']):
            props = feature['properties']
            
            if props.get('amenity') == 'school':
                props['tipo'] = 'escola'
                props['id'] = f"school_{i}" # ID ÚNICO
                props['alunos'] = random.randint(100, 800)
                props['orcamento_mensal'] = round(random.uniform(5000, 50000), 2)
                props['demanda_atual'] = random.choice(DEMANDAS_ESCOLA)
                processed_features.append(feature)
                
            elif props.get('landuse') in ['farmland', 'farm', 'orchard', 'meadow']:
                props['tipo'] = 'agricultor'
                props['id'] = f"farmer_{i}" # ID ÚNICO
                qtd_prod = random.randint(3, 5)
                props['produtos_disponiveis'] = random.sample(PRODUTOS_SAFRA, qtd_prod)
                props['tem_dap'] = True
                processed_features.append(feature)
        
        DB["features"] = processed_features
        print(f"✅ DADOS CARREGADOS! {len(processed_features)} itens.")
        
    except Exception as e:
        print(f"❌ ERRO AO CARREGAR: {e}")

# --- ROTA DE MAPA ---
@app.get("/geojson/enriched")
def get_map_data():
    return {"type": "FeatureCollection", "features": DB["features"]}

# --- ROTA DE MATCH ---
@app.get("/match/calculate")
def calculate_match(school_id: str):
    print(f"🔎 Calculando rota para: {school_id}")
    
    school = next((f for f in DB["features"] if f['properties'].get('id') == school_id), None)
    if not school:
        raise HTTPException(status_code=404, detail="Escola não encontrada")
    
    school_coords = (school['geometry']['coordinates'][1], school['geometry']['coordinates'][0])
    farmers = [f for f in DB["features"] if f['properties'].get('tipo') == 'agricultor']
    
    matches = []
    
    for farmer in farmers:
        farmer_coords = (farmer['geometry']['coordinates'][1], farmer['geometry']['coordinates'][0])
        dist_km = geodesic(school_coords, farmer_coords).km
        economia = max(0, 500 - (dist_km * 15))
        
        matches.append({
            "farmer_id": farmer['properties']['id'],
            "farmer_name": farmer['properties'].get('name', f"Sítio Familiar {farmer['properties']['id']}"),
            "distance": round(dist_km, 1),
            "savings": round(economia, 2),
            "products": farmer['properties']['produtos_disponiveis']
        })
    
    matches.sort(key=lambda x: x['distance'])
    
    return {
        "school_id": school_id,
        "best_match": matches[0] if matches else None,
        "alternatives": matches[1:4]
    }