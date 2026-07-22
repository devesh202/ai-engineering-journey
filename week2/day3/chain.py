import os 
import sys
from groq import Groq
from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)
model = "llama-3.3-70b-versatile"

JD = """
We are hiring a Backend Python Developer.

Requirements:
- Strong Python
- FastAPI or Django
- PostgreSQL
- Docker
- AWS
- REST APIs
- 2+ years of experience
"""
RESUME = """
Name: Rahul Sharma

Experience:
3 years as a Software Developer.

Skills:
Python, FastAPI, MySQL, Docker,
REST APIs, Git

Projects:
Built a food delivery backend using
FastAPI and MySQL.

Deployed applications using Docker.
"""

def ask_llm(system_prompt,user_prompt):
    message_system = {
     "role": "system",
     "content":system_prompt 
    }
    message_user = {
     "role": "user",
     "content":user_prompt 
    }
    messages = [message_system,message_user]
    response = client.chat.completions.create(model=model, messages=messages)
    answer = response.choices[0].message.content
    return answer

def step1_res_extract():
    system_prompt = f"""
    You are a professional HR assistant. Extract the skills from the candidate resume provided.
    Only return the skills no other information.do not invent any skills by yourself.
    """

    user_prompt = f"""
    Extract the skills from this resume {RESUME}"""
    return ask_llm(system_prompt,user_prompt)

def step2_jd_extract():
    system_prompt = """
    You are a professional HR assistant. Extract the skills from the job description provided.
    Only return the skills no other information.do not invent any skills by yourself.
    output format : 
    list of skills comma seperated dont return any filler info.
    """

    user_prompt = f"""
    Extract the skills from this job description {JD}"""
    return ask_llm(system_prompt,user_prompt)

def step3_match(candidate,jd):
    system_prompt = """
    You are a professional HR assistant. Compare the skills of the candidate and the skills required in the job description and produce a final score between 0 and 100. 
    Also produce a short final verdict whether the candidate is suitable for the job
   """
    user_prompt = f"""
    Compare the skills of the candidate {candidate} and the skills required in the job description {jd}
    """
    return ask_llm(system_prompt,user_prompt)
import time
candidate  = step1_res_extract()
print(candidate)
time.sleep(5) 

jd = step2_jd_extract()
print(jd)
time.sleep(5)

score =  step3_match(candidate,jd)

print(score)


