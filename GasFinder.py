import requests
from geopy.distance import geodesic

class GasFinder:
    def __init__(self, fuel_type, city):
        self.fuel_type = fuel_type
        self.city = city
        self.coordinates = None

    def get_coordinates(self):
        # Richiesta all'API di OpenStreetMap per ottenere le coordinate del paese
        url = f"https://nominatim.openstreetmap.org/search?q={self.city}&format=json"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data:
                self.lon = float(data[0]['lon'])
                self.lat = float(data[0]['lat'])
    
    def find_nearest(self):
        self.get_coordinates()
        if self.coordinates is None:
            raise ValueError("Coordinate non disponibili. Eseguire 'get_coordinates()' prima.")
        
        nearest = None
        
        query = f"SELECT *, (6371 * acos(cos(radians({self.lat})) * cos(radians(latitudine)) * cos(radians(longitudine) - radians({self.lon})) + sin(radians({self.lat})) * sin(radians(latitudine)))) AS distanza FROM locations ORDER BY distanza LIMIT 1;"

        result = self.db.execute_query(query)

        if result:
            # Estraggo il nome del benzinaio più vicin
            nearest = result[0][0]
            return nearest
