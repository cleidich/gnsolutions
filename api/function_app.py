import azure.functions as func
import logging
import requests
import os

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="getGoodNightMessage")
def get_gn_msg(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing a Good Night message request.')

    try:
        # Retrieve the OpenAI API key from environment variables
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if not openai_api_key:
            return func.HttpResponse("API key is missing", status_code=500)
        
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
            return func.HttpResponse(message, status_code=200, mimetype='text/plain')
        else:
            error_message = f"API request failed with status {response.status_code}: {response.text}"
            return func.HttpResponse(error_message, status_code=response.status_code, mimetype='text/plain')

    except Exception as e:
        logging.error("An error occurred:", exc_info=True)
        return func.HttpResponse(f"An unexpected error occurred: {str(e)}", status_code=500, mimetype='text/plain')