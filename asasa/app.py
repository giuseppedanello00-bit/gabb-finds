from flask import Flask, render_template, jsonify
import urllib.request
import csv
import io

app = Flask(__name__)

# Inserisci qui l'ID del tuo Google Sheet (preso dall'URL)
GOOGLE_SHEET_ID = "IL_TUO_ID_GOOGLE_SHEET_QUI"

# URL di esportazione CSV pubblica da Google Sheets
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/export?format=csv"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/products')
def get_products():
    try:
        # Se non hai ancora inserito l'ID del foglio, carica i dati locali di riserva
        if GOOGLE_SHEET_ID == "IL_TUO_ID_GOOGLE_SHEET_QUI":
            import json
            with open('products.json', 'r', encoding='utf-8') as f:
                return jsonify(json.load(f))

        # Scarica i dati dal foglio Google
        req = urllib.request.urlopen(SHEET_URL)
        csv_text = req.read().decode('utf-8')
        
        # Converte il formato CSV in una lista di dizionari JSON
        reader = csv.DictReader(io.StringIO(csv_text))
        products = []
        for row in reader:
            products.append({
                "id": int(row.get("id", 0)) if row.get("id") else 0,
                "name": row.get("name", ""),
                "category": row.get("category", "").strip().lower(),
                "brand": row.get("brand", "").strip(),
                "price": row.get("price", ""),
                "img": row.get("img", "https://via.placeholder.com/200"),
                "link": row.get("link", "#")
            })
            
        return jsonify(products)
    
    except Exception as e:
        print(f"Errore nella lettura da Google Sheets: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)