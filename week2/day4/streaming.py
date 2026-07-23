import os 
import sys
from groq import Groq
from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)
model = "llama-3.3-70b-versatile"
prompt = "What is internet"

message = {
    "role":"user",
    "content":prompt
}
messages = [message]
response = client.chat.completions.create(model=model, messages=messages, stream=True)
for chunk in response:
    content = chunk.choices[0].delta.content
    if content:
        print(content, end="", flush=True)