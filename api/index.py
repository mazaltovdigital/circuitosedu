import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Memória temporária para feedbacks (Reinicia se o servidor da Vercel hibernar)
feedbacks_lista = []

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message', '')
    api_key = os.environ.get('GEMINI_API_KEY', '').strip()
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": f"Você é um tutor pedagógico mediador de Circuitos CA para o mestrado de Daniel Sandoval. Ajude o aluno a pensar, não dê apenas a resposta: {user_input}"}]}]
    }
    
    try:
        response = requests.post(url, json=payload, timeout=20)
        reply = response.json()['candidates'][0]['content']['parts'][0]['text']
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": "Tive um problema na conexão. Pode repetir a dúvida?"})

@app.route('/api/feedback', methods=['POST'])
def salvar_feedback():
    dados = request.get_json()
    feedbacks_lista.append(dados)
    return jsonify({"status": "sucesso"}), 200

@app.route('/api/admin/feedbacks', methods=['POST'])
def listar_feedbacks():
    senha = request.get_json().get('password')
    # Senha de acesso ao painel
    if senha == "Mestrado2026":
        return jsonify(feedbacks_lista), 200
    return jsonify({"erro": "Acesso negado"}), 403

@app.route('/')
def home():
    return jsonify({"status": "Backend CircuitosEdu Operacional"}), 200
