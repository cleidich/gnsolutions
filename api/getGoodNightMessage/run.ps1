using namespace System.Net

# Input bindings are passed in via param block.
param($Request, $TriggerMetadata)

$openaiApiKey = $env:OPENAI_API_KEY

# Construct the OpenAI API request payload
$apiUrl = "https://api.openai.com/v1/chat/completions"
$requestBody = @{
    model = "gpt-4"
    messages = @(
        @{
            role = "developer"
            content = "You're instructed to generate silly or over-the-top Good Night greetings. Sarcasm is also encouraged. Each greeting should begin with 'GN (RandomName)!'"
        },
        @{
            role = "user"
            content = "Write a good night message."
        }
    )
} | ConvertTo-Json -Depth 10

$headers = @{
    "Authorization" = "Bearer $openaiApiKey"
    "Content-Type" = "application/json"
}

try {
    # Send the HTTP request to the OpenAI API
    $response = Invoke-RestMethod -Uri $apiUrl -Method Post -Headers $headers -Body $requestBody -ContentType "application/json"

    # Extract the generated message from the API response
    $message = $response.choices[0].message.content

    Push-OutputBinding -Name Response -Value @{ statuscode = 200; body = $message }
} catch {
    Push-OutputBinding -Name Response -Value @{ statuscode = 500; body = @{ error = "Failed to generate message: $($_.Exception.Message)" } }
}
