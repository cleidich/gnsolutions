import os
import json
import logging
import requests
from flask import Flask, request, jsonify

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def generate_message():
    """
    Endpoint to generate a message using OpenAI's GPT-4 API.
    """
    try:
        # Retrieve the OpenAI API key from environment variables
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if not openai_api_key:
            return jsonify({"error": "API key is missing"}), 500

        # Define the API URL and headers
        api_url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {openai_api_key}",
            "Content-Type": "application/json"
        }

        # Define the request payload
        request_body = {
            "model": "gpt-4",
            "messages": [
                {
                    "role": "developer",
                    "content": "You're instructed to generate silly or over-the-top Good Night greetings. Sarcasm is also encouraged. Each greeting should begin with 'GN (RandomName)!'"
                },
                {
                    "role": "user",
                    "content": "Write a good night message."
                }
            ]
        }

        # Send the HTTP POST request
        response = requests.post(api_url, headers=headers, json=request_body)

        # Check for a successful response
        if response.status_code == 200:
            response_data = response.json()
            message = response_data['choices'][0]['message']['content']
            return message, 200
        else:
            return jsonify({"error": f"API request failed with status {response.status_code}: {response.text}"}), response.status_code

    except Exception as e:
        logging.error("An error occurred:", exc_info=True)
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
