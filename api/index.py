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
    
    # URL estável para 2026: Gemini 2.0 Flash
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    payload = {
        "contents":}]
    }
    
    try:
        response = requests.post(url, json=payload, timeout=20)
        result = response.json()
        reply = result['candidates']['content']['parts']['text']
        return jsonify({"reply": reply}), 200
    except Exception as e:
        return jsonify({"reply": "O Tutor está processando muitas dúvidas agora. Tente em instantes."}), 200

@app.route('/api/feedback', methods=)
def feedback():
    # Rota operacional para receber dados de pesquisa
    return jsonify({"status": "sucesso"}), 200

@app.route('/')
def home():
    return jsonify({"status": "online"}), 200
