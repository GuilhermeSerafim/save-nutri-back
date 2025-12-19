import json
import random
from pathlib import Path

class DataService:
    """Responsável por carregar e gerenciar os dados do GeoJSON."""
    # Banco de dados em memória (Singleton-like para o MVP)
    _db = {"features": []}

    async def load_initial_data(self):
        """Lê o arquivo de Teresópolis e enriquece os dados."""
        file_path = Path("data/TeresopolisEscolasELocaisDeProducao.geojson")
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
            
            processed = []
            PRODUTOS = ["Alface", "Couve", "Tomate", "Cenoura", "Beterraba", "Inhame", "Brócolis", "Caqui"]
            DEMANDAS = ["Hortifruti Variado", "Legumes", "Frutas da Estação", "Folhosas"]

            for i, feature in enumerate(raw_data['features']):
                props = feature['properties']
                # Lógica de enriquecimento (Escolas)
                if props.get('amenity') == 'school':
                    props.update({
                        "tipo": "escola", "id": f"school_{i}",

                       # Inicialmente mockado
                        "alunos": random.randint(100, 800),
                        "orcamento_mensal": round(random.uniform(5000, 50000), 2),
                        "demanda_atual": random.choice(DEMANDAS)
                    })
                    processed.append(feature)
                # Lógica de enriquecimento (Agricultores)
                elif props.get('landuse') in ['farmland', 'farm', 'orchard', 'meadow']:
                    props.update({
                        "tipo": "agricultor", "id": f"farmer_{i}",
                        
                        # Inicialmente mockado
                        "produtos_disponiveis": random.sample(PRODUTOS, random.randint(3, 5)),
                        "tem_dap": True
                    })
                    processed.append(feature)

            self._db["features"] = processed
            print(f"✅ {len(processed)} registros carregados com sucesso.")
        except Exception as e:
            print(f"❌ Erro ao carregar GeoJSON: {e}")

    def get_all_features(self):
        return self._db["features"]

    def get_feature_by_id(self, feature_id: str):
        return next((f for f in self._db["features"] if f['properties'].get('id') == feature_id), None)