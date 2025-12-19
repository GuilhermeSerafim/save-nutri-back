from fastapi import APIRouter, HTTPException, Depends
from app.services.data_service import DataService
from app.services.location_service import LocationService # Note o _ no nome

router = APIRouter()

# Core do produto (mt usado no front)
@router.get("/calculate")
def calculate_match(
    school_id: str, 
    data_service: DataService = Depends(),
    loc_service: LocationService = Depends()
):
    """Calcula os melhores agricultores para uma escola específica."""
    school = data_service.get_feature_by_id(school_id)
    if not school:
        raise HTTPException(status_code=404, detail="Escola não encontrada")
    
    s_coords = (school['geometry']['coordinates'][1], school['geometry']['coordinates'][0])
    all_features = data_service.get_all_features()
    farmers = [f for f in all_features if f['properties'].get('tipo') == 'agricultor']
    
    matches = []
    for farmer in farmers:
        f_coords = (farmer['geometry']['coordinates'][1], farmer['geometry']['coordinates'][0])
        dist = loc_service.calculate_distance(s_coords, f_coords)
        savings = loc_service.calculate_savings(dist)
        
        matches.append({
            "farmer_id": farmer['properties']['id'],
            "farmer_name": farmer['properties'].get('name', f"Sítio Familiar {farmer['properties']['id']}"),
            "distance": round(dist, 1),
            "savings": round(savings, 2),
            "products": farmer['properties']['produtos_disponiveis']
        })
    
    matches.sort(key=lambda x: x['distance'])
    return {"school_id": school_id, "best_match": matches[0], "alternatives": matches[1:4]}