import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI( base_url="https://api.groq.com/openai/v1",
    api_key= os.environ.get("GROQ_API_KEY"))

messages = []

while True:
    user_input = input("You ->  ")
    if user_input.strip().lower() in ("exit","quit"):
        break

    messages.append({"role":"user","content": user_input})

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages
    )
    
    print(f"Agentic : {response.choices[0].message.content}")