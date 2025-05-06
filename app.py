from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS

# === Grammar check API ===
@app.route('/check', methods=['POST'])
def grammar_check():
    data = request.json
    user_text = data.get('text', '')
    language = data.get('language', 'en-AU')

    if not user_text:
        return jsonify({'message': 'No text provided.'}), 400

    payload = {
        'text': user_text,
        'language': language
    }

    response = requests.post('https://api.languagetool.org/v2/check', data=payload)

    if response.status_code != 200:
        return jsonify({'message': 'LanguageTool API failed.'}), 500

    response_data = response.json()

    matches = response_data.get('matches', [])
    if matches:
        message = matches[0].get('message', 'Issue found but no message provided.')
    else:
        message = 'No issues found.'

    return jsonify(message=message)

# === Serve the grammar-check.html page ===
@app.route('/grammar')
def serve_grammar_checker():
    return send_from_directory('static', 'grammar-check.html')

# === Default route ===
@app.route('/', methods=['GET'])
def home():
    return 'SLMS LanguageTool API is running.', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)