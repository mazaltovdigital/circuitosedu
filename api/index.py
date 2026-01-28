import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def get_gemini_response(user_input):
    api_key = os.environ.get('GEMINI_API_KEY', '').strip()
    if not api_key:
        return "Erro: GEMINI_API_KEY não configurada."

    # Lista de tentativas para evitar o erro 404
    tentativas = [
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}",
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}",
        f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    ]

    payload = {
        "contents": [{"parts": [{"text": f"Você é um tutor de Circuitos CA. Responda de forma pedagógica: {user_input}"}]}]
    }

    ultimo_erro = ""
    for url in tentativas:
        try:
            response = requests.post(url, json=payload, timeout=20)
            if response.status_code == 200:
                return response.json()['candidates'][0]['content']['parts'][0]['text']
            ultimo_erro = response.text
        except Exception as e:
            ultimo_erro = str(e)

    return f"Erro final após testar todas as rotas: {ultimo_erro}"

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    return jsonify({"reply": get_gemini_response(data.get('message', ''))})

@app.route('/')
def home():
    return jsonify({"status": "Tutor Online", "engine": "Gemini 1.5 Flash Multi-Route"}), 200
