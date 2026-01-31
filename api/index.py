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
    
    # URL para o modelo estável mais recente
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": f"Você é o mediador pedagógico do CircuitosEdu. Use andaimes pedagógicos para ensinar circuitos CA: {user_msg}"}]}]
    }
    
    try:
        response = requests.post(url, json=payload, timeout=15)
        result = response.json()
        # Verificando se a cota foi atingida (Erro 429) ou se o Google barrou
        if response.status_code!= 200:
             return jsonify({"reply": "Cota da IA atingida ou Billing inativo."}), 200
        
        reply = result['candidates']['content']['parts']['text']
        return jsonify({"reply": reply}), 200
    except Exception:
        return jsonify({"reply": "Tutor temporariamente offline."}), 200

@app.route('/api/feedback', methods=)
def handle_feedback():
    return jsonify({"status": "success"}), 200
