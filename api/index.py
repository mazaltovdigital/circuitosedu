import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Memória temporária para feedbacks (Sessions)
feedbacks_lista = []

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message', '')
    api_key = os.environ.get('GEMINI_API_KEY', '').strip()
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": f"Você é um tutor pedagógico mediador de Circuitos CA. Ajude o aluno a refletir sobre os conceitos físicos: {user_input}"}]}]
    }
    
    try:
        response = requests.post(url, json=payload, timeout=15)
        reply = response.json()['candidates'][0]['content']['parts'][0]['text']
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": "Ops! Tive um problema de conexão. Pode tentar novamente?"})

@app.route('/api/feedback', methods=['POST'])
def salvar_feedback():
    dados = request.get_json()
    feedbacks_lista.append(dados)
    return jsonify({"status": "sucesso"}), 200

@app.route('/api/admin/feedbacks', methods=['POST'])
def listar_feedbacks():
    senha = request.get_json().get('password')
    # Senha definida conforme sua preferência para o painel
    if senha == "Mestrado2026":
        return jsonify(feedbacks_lista), 200
    return jsonify({"erro": "Acesso negado"}), 403

@app.route('/')
def home():
    return jsonify({"status": "Servidor CircuitosEdu Online"}), 200
