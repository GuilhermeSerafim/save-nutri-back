from fastapi import APIRouter, Depends
from app.services.data_service import DataService

router = APIRouter()

@router.get("/enriched")
def get_map_data(service: DataService = Depends()):
    """Retorna o GeoJSON completo e enriquecido para o mapa."""
    features = service.get_all_features()
    return {"type": "FeatureCollection", "features": features}