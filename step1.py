import os
from openai import OpenAI
from dotenv import load_dotenv
from config import MODEL_LLM

load_dotenv()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key= os.environ.get("GROQ_API_KEY")
)

response = client.chat.completions.create(
    model=MODEL_LLM,
    messages=[
        {
            "role": "user",
            "content": "what is 1-1?"
        }
    ]
)

print(response.choices[0].message.content)