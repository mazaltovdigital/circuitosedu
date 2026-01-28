import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def get_gemini_response(user_input):
    # O código agora busca a variável GEMINI_API_KEY
    api_key = os.environ.get('GEMINI_API_KEY', '').strip()
    if not api_key:
        return "Erro: Chave GEMINI_API_KEY não configurada na Vercel."

    # Usando o modelo Gemini 1.5 Flash (Gratuito e estável)
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{"text": f"Você é um tutor pedagógico de Circuitos CA. Responda: {user_input}"}]
        }]
    }

    try:
        response = requests.post(url, json=payload, timeout=30)
        data = response.json()
        
        if response.status_code == 200:
            return data['candidates'][0]['content']['parts'][0]['text']
        return f"Erro no Google (Status {response.status_code}): {data.get('error', {}).get('message', 'Erro desconhecido')}"
    except Exception as e:
        return f"Erro de conexão: {str(e)}"

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    return jsonify({"reply": get_gemini_response(data.get('message', ''))})

@app.route('/')
def home():
    return jsonify({"status": "Tutor Gemini Online"}), 200
