import requests
import json
from GasFinder import GasFinder

class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{self.token}"
        self.gas_finder = GasFinder(None, None)
        self.offset = None

    def send_message(self, chat_id, text):
        url = f"{self.base_url}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': text
        }
        response = requests.post(url, json=data)
        if response.status_code != 200:
            print("Errore durante l'invio del messaggio.")
        else:
            print(f"SENT({text})")

    def handle_message(self, message):
        chat_id = message['chat']['id']
        text = message['text']
        print(f"RECEIVED({text})")

        if text.lower() == "/start":
            self.send_message(chat_id, "Inserisci il tipo di carburante (benzina, diesel)")
        elif not self.gas_finder.fuel_type:
            self.gas_finder.fuel_type = text
            self.send_message(chat_id, "Inserisci il nome della posizione in cui ti trovi (preferibilmente paese)")
        elif not self.gas_finder.city:
            self.gas_finder.city = text
            self.gas_finder.get_coordinates()
            gas_stations = [
    {'fuel_type': 'gasolio', 'longitude': '12.4923', 'latitude': '41.8902'},
    {'fuel_type': 'benzina', 'longitude': '12.4861', 'latitude': '41.8947'},
    {'fuel_type': 'diesel', 'longitude': '12.4878', 'latitude': '41.8955'},
    {'fuel_type': 'gasolio', 'longitude': '12.4987', 'latitude': '41.8921'},
]
            nearest_station = self.gas_finder.find_nearest_gas_station(gas_stations)
            if nearest_station:
                self.send_message(chat_id, f"Il distributore più vicino è: {nearest_station['longitude']} {nearest_station['latitude']}")
            else:
                self.send_message(chat_id, "Nessun distributore trovato.")
            self.gas_finder = GasFinder(None, None)

    """
    def handle_message(self, message):
        chat_id = message['chat']['id']
        text = message['text']
        print(f"RECEIVED({text})")

        if not self.gas_finder.fuel_type:
            self.gas_finder.fuel_type = text
            self.send_message(chat_id, "Inserisci il paese:")
        elif not self.gas_finder.city:
            self.gas_finder.city = text
            self.gas_finder.get_coordinates()
            gas_stations = [
    {'fuel_type': 'gasolio', 'longitude': '12.4923', 'latitude': '41.8902'},
    {'fuel_type': 'benzina', 'longitude': '12.4861', 'latitude': '41.8947'},
    {'fuel_type': 'diesel', 'longitude': '12.4878', 'latitude': '41.8955'},
    {'fuel_type': 'gasolio', 'longitude': '12.4987', 'latitude': '41.8921'},
]  # Metodo per ottenere la lista dei distributori di carburante
            nearest_station = self.gas_finder.find_nearest_gas_station(gas_stations)
            if nearest_station:
                self.send_message(chat_id, f"Il distributore più vicino è: {nearest_station['fuel_type']}")
            else:
                self.send_message(chat_id, "Nessun distributore trovato.")
            self.gas_finder = GasFinder(None, None)
    """
    """
    def get_updates(self):
        url = f"{self.base_url}/getUpdates"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(data)
            for update in data['result']:
                if self.last_id < int(data['result'][0]['update_id']):
                    self.last_id = int(data['result'][0]['update_id'])
                    print(update)
                    print(data['result'][0]['message']['text'])
                    #if self.offset == data['']
                    #self.handle_message(update['update_id'], update['message'])
    """
    
    def get_updates(self):
        url = f"{self.base_url}/getUpdates"
        params = {'offset': self.offset, 'timeout': 5}  # Aggiunta: impostiamo il timeout a 5 secondi
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            for update in data['result']:
                self.offset = update['update_id'] + 1  # Aggiunta: aggiorniamo l'offset all'ultimo messaggio + 1
                self.handle_message(update['message'])

    def run(self):
        print("Waiting for messages")
        while True:
            self.get_updates()
    
    def get_gas_stations():
        return [
        {'fuel_type': 'gasolio', 'longitude': '12.4923', 'latitude': '41.8902'},
        {'fuel_type': 'benzina', 'longitude': '12.4861', 'latitude': '41.8947'},
        {'fuel_type': 'diesel', 'longitude': '12.4878', 'latitude': '41.8955'},
        {'fuel_type': 'gasolio', 'longitude': '12.4987', 'latitude': '41.8921'},]
