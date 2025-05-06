from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/check', methods=['POST'])
def check_text():
    # Get JSON data from Leap
    data = request.get_json()

    # Extract the text and language
    text = data.get('text', '')
    language = data.get('language', 'en-AU')

    # Call LanguageTool API
    lt_api_url = 'https://api.languagetool.org/v2/check'
    payload = {
        'text': text,
        'language': language
    }
    response = requests.post(lt_api_url, data=payload)

    if response.status_code != 200:
        return jsonify({'error': 'LanguageTool API error', 'details': response.text}), 500

    response_data = response.json()

    # Flatten the response: get the first message only
    matches = response_data.get('matches', [])
    if matches:
        message = matches[0].get('message', 'Issue found but no message provided.')
    else:
        message = 'No issues found.'

    # Return a simple JSON response
    return jsonify(message=message)

@app.route('/', methods=['GET'])
def home():
    return 'SLMS LanguageTool API is running.', 200

if __name__ == '__main__':
    app.run(debug=True)