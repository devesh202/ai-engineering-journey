import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set")
client = Groq(api_key=GROQ_API_KEY)
model = "llama-3.3-70b-versatile"

prompt = "What is weather in dombivli today will it rain?"
message={
    "role": "user",
    "content": prompt
}
messages=[message]
response = client.chat.completions.create(model=model, messages=messages)
print(response.choices[0].message.content)


