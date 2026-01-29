import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message', '')
    api_key = os.environ.get('GEMINI_API_KEY', '').strip()
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": f"Você é um tutor pedagógico de Circuitos CA. Ajude o aluno de forma clara e didática: {user_input}"}]}]
    }
    
    try:
        response = requests.post(url, json=payload, timeout=20)
        reply = response.json()['candidates'][0]['content']['parts'][0]['text']
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": "Desculpe, tive um problema técnico. Pode repetir?"})

@app.route('/')
def home():
    return jsonify({"status": "Backend CircuitosEdu Ativo"}), 200
