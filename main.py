from DatabaseConnection import DatabaseConnection
from CSVImporter import CSVImporter
from TelegramBot import TelegramBot

def main():
    # Connessione al database
    db = DatabaseConnection()

    # URL del file CSV da scaricare
    prices_url = 'https://www.mimit.gov.it/images/exportCSV/prezzo_alle_8.csv'

    # Creazione dell'importer e importazione dei dati
    importer = CSVImporter(db)
    importer.import_prices(prices_url)

    locations_url = 'https://www.mimit.gov.it/images/exportCSV/anagrafica_impianti_attivi.csv'
    importer.import_locations(locations_url)

    #importer.import_locations(locations_url)

    TOKEN = '5808645926:AAHD1vdf8PBrUM1Gc-6dEqO8VTjGnzImvDI'
    # Esempio di utilizzo del bot
    bot = TelegramBot(TOKEN)
    bot.run()

if __name__ == '__main__':
    main()