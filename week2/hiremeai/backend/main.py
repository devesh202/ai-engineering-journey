from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pathlib import Path
from pypdf import PdfReader
from dotenv import load_dotenv
import os
from pathlib import Path
from groq import Groq
import json
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set")
client = Groq(api_key=GROQ_API_KEY)
model = "llama-3.3-70b-versatile"
#pdf extraction
def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
    
       page_text = page.extract_text()
       if page_text:
        text += page_text + "\n"
        

    return text
from pydantic import BaseModel

class Experience(BaseModel):
    company:str| None=None
    role: str| None=None
    duration: str| None=None
    description:str| None=None
    skills_used: list[str] | None = None

class Resume(BaseModel):
    name:str| None=None
    email:str| None=None
    phone:str| None=None
    total_exp_years : float | None = None
    skills:list[str]=[]
    experiences: list[Experience]=[]
    education: list[str]=[]
    projects: list[str]=[]
    certification : list[str] = []

resume_schema = Resume.model_json_schema()
class ChatRequest(BaseModel):
    question: str
#ask candidate
def ask_candidate(question: str, resume: Resume):
    system_prompt = f"""
You are an AI assistant representing a job candidate.

Below is everything you know about the candidate.

{resume.model_dump_json(indent=2)}

Rules:

1. Answer only using this information.

2. Never hallucinate.

3. If information is unavailable,
say

"I don't have enough information to answer that."

4. Be professional.

5. Answer as if HR is interviewing this candidate.
"""

    stream = client.chat.completions.create(

        model=model,

        messages=[

            {
                "role":"system",
                "content":system_prompt
            },

            {
                "role":"user",
                "content":question
            }

        ],
        stream=True
    )

    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            yield content
    
#parsing resume
def parse_resume(resume_text):
    system_prompt = f"""
    You are an expert resume parser.

    Extract information from the resume based on its meaning,
    not only based on exact section headings.

    Different resumes may use different headings.

    For example:
    - Experience
    - Professional Experience
    - Work History
    - Employment
    - Internships

    These may all contain relevant experience.

    Skills may also appear in the skills section, work experience,
    internships or projects.

    Return ONLY valid JSON matching this schema:

    {resume_schema}

    Important rules:

    1. Do not invent information.
    2. If a value is not available, return null.
    3. If a list has no information, return an empty list.
    4. Include internships inside experiences.
    5. Extract skills mentioned across the entire resume.
    """
    user_prompt = f"""
    Parse the following resume:

    {resume_text}
    """
    message_system={
        "role" : "system",
        "content" : system_prompt
    }
    message_user={
        "role" : "user",
        "content" : user_prompt
    }
    messages=[message_system, message_user]
    response_format={
        "type": "json_object"
    }
    response=client.chat.completions.create(model=model, messages=messages, response_format=response_format)
    raw_output = response.choices[0].message.content
    data = json.loads(raw_output)
    resume = Resume(**data)
    return resume

@app.get("/") 

def home():
    resume_text = read_pdf(Path("resume.pdf"))
    resume = parse_resume(resume_text)
    print(resume.model_dump_json(indent=2))
    return {
        "message": "resume parsed successfully"
    }

_resume_cache = None

def get_resume():
    global _resume_cache
    if _resume_cache is None:
        resume_text = read_pdf(Path("resume.pdf"))
        _resume_cache = parse_resume(resume_text)
    return _resume_cache

@app.post("/chat")
def chat(request: ChatRequest):
    resume = get_resume()
    return StreamingResponse(
        ask_candidate(request.question, resume),
        media_type="text/plain",
    )