import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from config import MODEL_LLM

load_dotenv()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("GROQ_API_KEY"),
)

def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file '{path}': {e}"

AVAILABLE_TOOLS = {
    "read_file": read_file,
}

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the text contents of a specified file path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The path of the file to read (e.g. 'notes.txt')",
                    }
                },
                "required": ["path"],
            },
        },
    }
]

messages = [
    {
        "role": "system",
        "content": "You are a helpful coding assistant. You have access to local tools. Do not invent tools that are not provided in the tool schemas.",
    }
]

while True:
    user_input = input("You ->  ")
    if user_input.strip().lower() in ("exit", "quit"):
        break

    messages.append({"role": "user", "content": user_input})

    while True:
        response = client.chat.completions.create(
            model=MODEL_LLM,
            messages=messages,
            tools=TOOL_SCHEMAS,
        )

        response_message = response.choices[0].message
        messages.append(response_message)

        if not response_message.tool_calls:
            print(f"Agentic : {response_message.content}")
            break

        for tool_call in response_message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments or "{}")

            if tool_name in AVAILABLE_TOOLS:
                tool_output = AVAILABLE_TOOLS[tool_name](**tool_args)
            else:
                tool_output = f"Error: Tool '{tool_name}' is not available."

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_name,
                "content": str(tool_output),
            })