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
    
    # Migração para Gemini 3 Flash (GA 2026) para evitar erros de descontinuação
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": f"Você é o tutor mediador do CircuitosEdu. Use scaffolding pedagógico para ensinar: {user_msg}"}]}]
    }
    
    try:
        response = requests.post(url, json=payload, timeout=20)
        # Tratamento de faturamento/Billing
        if response.status_code == 429:
            return jsonify({"reply": "Limite atingido. Verifique o Billing no Google AI Studio."}), 200
            
        result = response.json()
        reply = result['candidates']['content']['parts']['text']
        return jsonify({"reply": reply}), 200
    except Exception:
        return jsonify({"reply": "Mediador IA temporariamente offline."}), 200

@app.route('/')
def home():
    return jsonify({"status": "online"}), 200
