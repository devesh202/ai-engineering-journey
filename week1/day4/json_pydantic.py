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
role="user"
#structure it using pydantic
from pydantic import BaseModel
class Ticket(BaseModel):
    name: str
    email: str
    issue: str
schema = Ticket.model_json_schema()
response_format = {
    "type": "json_object" 
}
system_prompt =  f"""
extract the personal information from the ticket strictly based on this schema {schema} and give me json output.
"""

text = "Hello i am devesh . I have purchased iphone which is not working at all. ankita is my gf. My address is delhi.my email is abc@gmail.com. My contact no. is 1234567890"
prompt = f"""

This is a customer ticket and please extract the personal information from this. {text}
"""
message ={
    "role":role,
    "content":prompt
}
message_system = {
 "role": "system",
 "content":system_prompt 
}
messages = [message_system,message]

response = client.chat.completions.create(model=model, messages=messages,response_format=response_format)
answer = response.choices[0].message.content
print(answer)

import json
raw_json = answer
data_file = json.loads(raw_json)
ticket = Ticket(**data_file)
print(ticket.name)
print(ticket.email)
print(ticket.issue)