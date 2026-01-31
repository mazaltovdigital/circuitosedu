import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/chat', methods=)
def chat():
    data = request.get_json()
    user_msg = data.get('message', '')
    api_key = os.environ.get('GEMINI_API_KEY', '').strip()
    
    # URL Estável para Gemini 1.5 Flash (v1) para evitar erro 404
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": f"Você é o mediador pedagógico do CircuitosEdu. Use andaimes pedagógicos: {user_msg}"}]}]
    }
    
    try:
        response = requests.post(url, json=payload, timeout=20)
        # Se retornar 429, significa que o Google exige Billing ativo
        if response.status_code == 429:
            return jsonify({"reply": "Cota excedida. Verifique se o Billing está ativo no Google Cloud."}), 200
            
        result = response.json()
        reply = result['candidates']['content']['parts']['text']
        return jsonify({"reply": reply}), 200
    except Exception:
        return jsonify({"reply": "Tutor IA temporariamente offline para manutenção."}), 200

@app.route('/')
def home():
    return jsonify({"status": "online"}), 200
