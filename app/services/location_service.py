from geopy.distance import geodesic

class LocationService:
    """Calcula distâncias e regras de match geográfico."""
    def calculate_distance(self, coord1, coord2):
        """Retorna distância em KM."""
        return geodesic(coord1, coord2).km

    def calculate_savings(self, dist_km):
        """Aplica fórmula de economia logística."""
        return max(0, 500 - (dist_km * 15))