import os 
import sys
from groq import Groq
from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)
model = "llama-3.3-70b-versatile"
# //tools
def get_product_price(product):
    if product == "Iphone 17":
        return 1000
    elif product == "Iphone 16":
        return 500
    else:
        return 0

def calculator(expression):
    try:
        return eval(expression)
    except:
        return "Invalid expression"
tools = {
    "get_product_price": get_product_price,
    "calculator": calculator
}

system_prompt = f"""
You are a shopping assistant.
You have these tools:
get_product_price(product)
calculator(expression)

IMPORTATNT:
call tools exactly like these examples:
Action : get_product_price("Iphone 17")
Action : calculator('3-2')
Never write:
get_product_price(product="Iphone 17")
Never write:
calculator(expression='3-2')
Follow these rules:
1.Decide what you need to do next.
2.Call only ONE tool at a time.
3.After writing an Action, STOP immediately.
4.Never gues or invent a tool result.
5.Wait untill you recieve an Observation
6.then decide your next action.
7.When the task is complete, give the Final Answer.

Format:
Thought : what you need to do
Action : tool_name(arguments)

When finished:
Final Answer: your answer
"""

import re
from time import sleep
def run_agent(question):
 messages = [{
     "role":"system",
     "content":system_prompt
 },
 {
     "role":"user",
     "content":question
 }]
 for step in range(5):
     print("\n -----------------")
     print("Step",step+1)
     print("-----------------")

     response = client.chat.completions.create(model=model, messages=messages, temperature=0)
     answer = response.choices[0].message.content
     print(answer)
     #Agent has finished
     if "Final Answer:" in answer:
         print(answer.split("Final Answer:")[1].strip())
         break
     
     #find the action
     match = re.search(
         r"Action\s*:\s*(\w+)\((.*?)\)",
         answer
     )

     if match:
         tool_name = match.group(1)
         tool_input = match.group(2)
         tool_input = tool_input.strip()
         tool_input = tool_input.strip("\"'")
        
         #run tool
         if tool_name in tools:
             tool = tools[tool_name]
             observation = tool(tool_input)
         else:
             observation = f"Unknown tool: {tool_name}"
         print("Observation:",observation)
     #   Add llm response to memory
         messages.append({
             "role":"assistant",
             "content":answer
         }) 

         #give tool result back to LLM
         messages.append({
             "role":"user",
             "content": f"Observation: {observation}"
         })
         sleep(5)


prompt = f"""
I have 5000 rupees. What is the price of Iphone 17?
and how much money will i have left?
"""
run_agent(prompt)