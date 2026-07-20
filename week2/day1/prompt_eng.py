import os 
import sys
from groq import Groq
from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)
model = "llama-3.3-70b-versatile"

def llm_ans(prompt):
    message = {
        "role":"user",
        "content":prompt
    }
    messages = [message]
    response = client.chat.completions.create(model=model, messages=messages)
    ans = response.choices[0].message.content
    return ans

bad_prompt = """
#Role:
You are a customer support assitant at laptop company.
#Task:
You have to classify the issue in a category
#constraint:
You have to classify the issue in one of 3 categories namely: billing,technical,return.
#Output format :
#  your ans should be in one word only and it should be one of the categories given in constraints
#Example : 
for instance, if user complain says he wants a refund then category is return
#Fallback :
if the issue is unrelated to any of the categories given in constraints then your ans should be : Other
this is a user complaint:
My gf left me.
"""

print(llm_ans(bad_prompt))