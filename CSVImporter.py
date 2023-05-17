import requests
import csv
from datetime import datetime

class CSVImporter:
    def __init__(self, db):
        self.db = db

    def download_csv(self, url):
        response = requests.get(url)
        response.raise_for_status()  # Genera un'eccezione se la richiesta non ha successo

        return response.text

    def import_prices(self, url):
        print("Downloading CSV")
        csv_data = self.download_csv(url).splitlines()

        # Apri una connessione al database
        connection = self.db.connection
        cursor = connection.cursor()

        print("Deleting previous values")
        cursor.execute("DELETE FROM prices")
        connection.commit()

        print("Preparing query")
        # Inserimento dei dati nel database
        insert_query = "INSERT INTO `prices` VALUES (%s, %s, %s, %s, %s)"
        #insert_query = "INSERT INTO `prices' VALUES (%s, %s, %s, %s, %s)"
        csv_reader = csv.reader(csv_data, delimiter=";")

        # Salta l'intestazione del CSV
        next(csv_reader)
        next(csv_reader)

        print("Adding values to database")

        for row in csv_reader:
            cursor.execute(insert_query, row)

        connection.commit()

        print("Updating settings...")

        setting_name = 'PRICES_LAST_UPDATED'
        setting_value = datetime.now()

        update_query = f"UPDATE `configuration` SET `value` = '{setting_value}' WHERE `configuration`.`name` = '{setting_name}'"

        # Esegui l'inserimento utilizzando il metodo execute_insert della classe DatabaseConnection
        cursor.execute(update_query)
        connection.commit()

        # Chiusura della connessione al database
        cursor.close()

        print("Done.")
    
    def import_locations(self, url):
        print("Downloading CSV")
        csv_data = self.download_csv(url).splitlines()

        # Apri una connessione al database
        connection = self.db.connection
        cursor = connection.cursor()

        print("Deleting previous values")
        cursor.execute("DELETE FROM locations")
        connection.commit()

        print("Preparing query")
        # Inserimento dei dati nel database
        insert_query = "INSERT INTO `locations` VALUES (%s)"
        csv_reader = csv.reader(csv_data, delimiter=";")

        # Salta l'intestazione del CSV
        next(csv_reader)
        next(csv_reader)

        print("Adding values to database")

        for row in csv_data:
            cursor.execute(insert_query, [row])

        connection.commit()

        print("Updating settings...")

        setting_name = 'LOCATIONS_LAST_UPDATED'
        setting_value = datetime.now()

        update_query = f"UPDATE `configuration` SET `value` = '{setting_value}' WHERE `configuration`.`name` = '{setting_name}'"

        # Esegui l'inserimento utilizzando il metodo execute_insert della classe DatabaseConnection
        cursor.execute(update_query)
        connection.commit()

        # Chiusura della connessione al database
        cursor.close()

        print("Done.")
