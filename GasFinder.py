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
                self.coordinates = (float(data[0]['lon']), float(data[0]['lat']))

    def find_nearest_gas_station(self, gas_stations):
        self.get_coordinates()
        if self.coordinates is None:
            raise ValueError("Coordinate non disponibili. Eseguire 'get_coordinates()' prima.")

        min_distance = float('inf')
        nearest_station = None

        for station in gas_stations:
            if station['fuel_type'] == self.fuel_type:
                station_coordinates = (float(station['longitude']), float(station['latitude']))
                distance = geodesic(self.coordinates, station_coordinates).km
                if distance < min_distance:
                    min_distance = distance
                    nearest_station = station

        return nearest_station

"""
fuel_type = 'gasolio'
city = 'Italia'
gas_stations = [
    {'fuel_type': 'gasolio', 'longitude': '12.4923', 'latitude': '41.8902'},
    {'fuel_type': 'benzina', 'longitude': '12.4861', 'latitude': '41.8947'},
    {'fuel_type': 'diesel', 'longitude': '12.4878', 'latitude': '41.8955'},
    {'fuel_type': 'gasolio', 'longitude': '12.4987', 'latitude': '41.8921'},
]

gas_finder = GasFinder(fuel_type, city)
gas_finder.get_coordinates()
nearest_station = gas_finder.find_nearest_gas_station(gas_stations)
print("Distributore più vicino:")
print(nearest_station)
"""
