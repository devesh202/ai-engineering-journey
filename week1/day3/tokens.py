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
# 3 prompts
prompt1 = 'Hi!'
prompt2 = "Explain time travel in detail"
prompt3='write a 1000 word essay on machine learning'

prompts = [prompt1, prompt2, prompt3]
for prompt in prompts:
    message = {
    "role":"user",
    "content":prompt
    }
    messages = [message]
#temperature by default is 0 and range is till 2
    response = client.chat.completions.create(model=model, messages=messages)
    usage = response.usage
    print(f"Prompt:{prompt}->Your tokens:{usage.prompt_tokens} completion_tokens:{usage.completion_tokens} total_tokens:{usage.total_tokens} Finish reason:{response.choices[0].finish_reason}")


# print(response.choices[0].message.
# content)
# print(response.usage.total_tokens)