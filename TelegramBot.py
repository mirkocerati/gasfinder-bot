import requests
import json
from DatabaseConnection import DatabaseConnection
from GasFinder import GasFinder

class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{self.token}"
        self.gas_finder = GasFinder(None, None)
        self.offset = None
        self.db = DatabaseConnection()

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
            nearest = self.gas_finder.find_nearest()
            if nearest:
                self.send_message(chat_id, f"Il distributore più vicino è: {nearest}")
            else:
                self.send_message(chat_id, "Nessun distributore trovato.")
            self.gas_finder = GasFinder(None, None)
    
    def get_updates(self):
        url = f"{self.base_url}/getUpdates"
        params = {'offset': self.offset, 'timeout': 5}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            for update in data['result']:
                self.offset = update['update_id'] + 1
                self.handle_message(update['message'])

    def run(self):
        print("Waiting for messages")
        while True:
            self.get_updates()
