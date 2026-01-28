import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# Permite que seu site no GitHub Pages fale com o servidor
CORS(app, resources={r"/*": {"origins": "*"}})

def get_response(user_input):
    # Busca a chave que você vai configurar na Vercel
    api_key = os.environ.get('PERPLEXITY_API_KEY', '').strip()
    if not api_key:
        return "Erro: PERPLEXITY_API_KEY não configurada."

    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.1-sonar-small-128k-online",
        "messages": [
            {"role": "system", "content": "Você é um tutor de Circuitos CA. Explique de forma clara."},
            {"role": "user", "content": user_input}
        ]
    }

    try:
        response = requests.post(url, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        return f"Erro na API (Status {response.status_code}): {response.text}"
    except Exception as e:
        return f"Erro de conexão: {str(e)}"

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    return jsonify({"reply": get_response(data.get('message', ''))})

@app.route('/')
def home():
    return jsonify({"status": "Servidor Perplexity Online"}), 200
