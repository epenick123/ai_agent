import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

if len(sys.argv)<2:
    print("Error:No prompt provided"),
    sys.exit(1)

messages = [
    types.Content(role="user", parts=[types.Part(text=sys.argv[1])]),
]

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")


client = genai.Client(api_key=api_key)

response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages
    )

if len(sys.argv)==2: 
    print(response.text)

elif sys.argv[2] == "--verbose":
    print("User prompt:", sys.argv[1])
    print("Prompt tokens:",response.usage_metadata.prompt_token_count)
    print("Response tokens:",response.usage_metadata.candidates_token_count)
    print(response.text)
else:
    print(response.text)


