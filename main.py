import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import get_files_info
from prompt import system_prompt
from call_function import available_functions

# This script uses the Google Gemini API to generate content based on a user-provided prompt.
# It requires the `google-genai` package and a valid API key stored in a `.env` file.
# Load environment variables from .env file
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
model_name = 'gemini-2.0-flash-001'

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
    config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt),
)

candidate = response.candidates[0]
fc = candidate.content.parts[0].function_call

if fc is not None:
    print(f"Calling function: {fc.name}({fc.args})")

# Print the response from the model
print(candidate.content.parts[0].text)

# If the user requested verbose output, print additional information
if ("--verbose" in sys.argv):
    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
