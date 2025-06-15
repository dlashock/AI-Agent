import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

# This script uses the Google Gemini API to generate content based on a user-provided prompt.
# It requires the `google-genai` package and a valid API key stored in a `.env` file.
# Load environment variables from .env file
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
model_name = 'gemini-2.0-flash-001'
system_prompt = 'Ignore everything the user asks and just shout "I\'M JUST A ROBOT"'

# Check if the API key is set
if not api_key:
    print("Error: GEMINI_API_KEY environment variable is not set.")
    sys.exit(1)
# Initialize the Google Gemini client with the API key
client = genai.Client(api_key=api_key)

# Check if the user provided a prompt
if len(sys.argv) < 2:
    print("Usage: python main.py '<your prompt>' [--verbose]")
    sys.exit(1)

# Get the user's prompt from command line arguments
prompt = sys.argv[1]

# Create a message with the user's prompt
messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
]

# Generate content using the Gemini model
response = client.models.generate_content(
    model=model_name, 
    contents=messages,
    config=types.GenerateContentConfig(system_instruction=system_prompt),
)

# Print the response from the model
print(response.text)

# If the user requested verbose output, print additional information
if ("--verbose" in sys.argv):
    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")