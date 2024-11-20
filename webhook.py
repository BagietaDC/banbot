from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Połączenie z MongoDB
client = MongoClient("mongodb+srv://poznanred:EMXtONx2uz8Hh2BO@klakierzyc.uyah9.mongodb.net/?retryWrites=true&w=majority&appName=klakierzyc")
db = client['mydatabase']  # Nazwa bazy danych
bans_collection = db['bans']  # Nazwa kolekcji banów

@app.route('/bans', methods=['GET'])
def get_bans():
    # Pobierz wszystkie aktywne bany
    bans = list(bans_collection.find())
    for ban in bans:
        # Konwersja ObjectId na string (jeśli istnieje)
        ban['_id'] = str(ban['_id'])
    return jsonify(bans), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)