from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/check', methods=['POST'])
def grammar_check():
    data = request.json
    user_text = data.get('text', '')
    language = data.get('language', 'en-AU')

    if not user_text:
        return jsonify({'error': 'No text provided'}), 400

    payload = {
        'text': user_text,
        'language': language
    }

    response = requests.post('https://api.languagetool.org/v2/check', data=payload)

    if response.status_code != 200:
        return jsonify({'error': 'LanguageTool API failed', 'details': response.text}), 500

    return response.json()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)