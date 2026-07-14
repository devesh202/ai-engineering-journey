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

prompt = "Suggest only one brand name for a food company."
message_system = {
    "role":"system",
    "content":"You are a brand manager who tells good brand names for food companies."
}

message = {
    "role":"user",
    "content":prompt
}
messages = [message_system, message]
#temperature by default is 0 and range is till 2
response = client.chat.completions.create(model=model, messages=messages, temperature=2)
print(response.choices[0].message.content)
print(response.usage.total_tokens)