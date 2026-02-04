import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_msg = data.get('message', '')
    api_key = os.environ.get('GEMINI_API_KEY', '').strip()
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": f"Você é o tutor mediador do CircuitosEdu. Use scaffolding pedagógico para ensinar: {user_msg}"}]}]
    }
    
    try:
        response = requests.post(url, json=payload, timeout=20)
        if response.status_code == 429:
            return jsonify({"reply": "Limite atingido. Tente novamente mais tarde."}), 200
            
        result = response.json()
        try:
            reply = result['candidates'][0]['content']['parts'][0]['text']
        except (KeyError, IndexError):
            reply = "Desculpe, não consegui processar sua resposta no momento."

        return jsonify({"reply": reply}), 200
    except Exception as e:
        print(f"Erro no chat: {e}")
        return jsonify({"reply": "Mediador IA temporariamente offline."}), 200

@app.route('/api/feedback', methods=['POST'])
def feedback():
    data = request.get_json()
    ajudou = data.get('ajudou')
    texto = data.get('texto')
    print(f"Feedback Recebido - Ajudou: {ajudou} | Comentário: {texto}")
    return jsonify({"status": "sucesso", "mensagem": "Feedback registrado"}), 200

@app.route('/')
def home():
    return jsonify({"status": "online"}), 200

if __name__ == '__main__':
    app.run(debug=True)
