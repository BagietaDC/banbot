from flask import Flask, jsonify, request
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# Połączenie z MongoDB
client = MongoClient("mongodb+srv://poznanred:EMXtONx2uz8Hh2BO@klakierzyc.uyah9.mongodb.net/?retryWrites=true&w=majority&appName=klakierzyc")
db = client['roblox_ban_system']  # Nazwa bazy danych
bans_collection = db['bans']  # Nazwa kolekcji banów

# Dodanie bana (POST)
@app.route('/ban', methods=['POST'])
def add_ban():
    """
    Dodaje nowy ban do systemu.
    Oczekuje: JSON z "username_or_id", "reason", "universe_id", "permanent", "hours".
    """
    data = request.get_json()
    
    # Weryfikacja wymaganych pól
    username_or_id = data.get("username_or_id")
    reason = data.get("reason")
    universe_id = data.get("universe_id")
    permanent = data.get("permanent", False)
    hours = data.get("hours", 0)

    if not username_or_id or not reason or not universe_id:
        return jsonify({"status": "error", "message": "Brak wymaganych danych"}), 400

    # Obliczanie daty zakończenia bana, jeśli nie jest permanentny
    ban_end = None if permanent else datetime.utcnow() + timedelta(hours=hours)

    # Tworzenie obiektu ban_entry
    ban_entry = {
        "username_or_id": username_or_id,
        "reason": reason,
        "permanent": permanent,
        "ban_end": ban_end,
        "universe_id": universe_id
    }

    # Wstawienie danych do MongoDB
    bans_collection.insert_one(ban_entry)

    return jsonify({"status": "success", "message": f"Gracz {username_or_id} został zbanowany w universe {universe_id}."}), 200


# Pobranie banów (GET) - filtracja według universe_id
@app.route('/bans', methods=['GET'])
def get_bans():
    """
    Pobiera wszystkie aktywne bany, opcjonalnie filtrując je według `universe_id`.
    """
    universe_id = request.args.get("universe_id")  # Pobranie `universe_id` z query string

    # Jeśli `universe_id` jest podane, filtrujemy bany tylko dla tego ID
    if universe_id:
        bans = list(bans_collection.find({"universe_id": universe_id}))
    else:
        # Jeśli nie podano `universe_id`, pobieramy wszystkie bany
        bans = list(bans_collection.find())

    # Konwersja ObjectId na string (jeśli istnieje)
    for ban in bans:
        ban['_id'] = str(ban['_id'])
        # Konwertowanie ban_end na string (jeśli jest ustawione)
        if ban['ban_end']:
            ban['ban_end'] = ban['ban_end'].isoformat()

    return jsonify(bans), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
