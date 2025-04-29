# imports
import os
import json
import requests
import ollama
import dotenv
from dotenv import load_dotenv
from IPython.display import DisplayHandle, Markdown, display, update_display
from openai import OpenAI

# constants
load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

if api_key and api_key.startswith('sk-proj-') and len(api_key)>10:
    print("API key looks good so far")
else:
    print("There might be a problem with your API key? Please visit the troubleshooting notebook!")
MODEL_GPT = 'gpt-4o-mini'
MODEL_LLAMA = 'llama3.2'

# set up environment
load_dotenv()
openai = OpenAI()

# here is the question; type over this to ask something new

question = """
Please explain what this code does and why:
yield from {book.get("author") for book in books if book.get("author")}
"""

# prompts
system_prompt = "You are a helpful technical tutor who answers questions about python code, software engineering, data science and LLMs"
user_prompt = "Please give a detailed explanation to the following question: " + question

# messages

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt}
]

# Get gpt-4o-mini to answer, with streaming

# ... your imports, dotenv loading, API‑key check, etc.

# 1) Stream the GPT response into a Python string
stream = openai.chat.completions.create(
    model=MODEL_GPT,
    messages=messages,
    stream=True
)
response = ""
for chunk in stream:
    # append each delta, skipping any None
    response += chunk.choices[0].delta.content or ''

# 2) (Optional) strip out any ``` fences or “markdown” tags
response = response.replace("```", "").replace("markdown", "")

# 3) Write it to a Markdown file
output_path = "explain.md"
with open(output_path, "w", encoding="utf-8") as md_file:
    md_file.write(response)

print(f"✅ Wrote full conversation to {output_path}\n")

# 4) Read it back and print to your terminal
with open(output_path, "r", encoding="utf-8") as md_file:
    print(md_file.read())

# Get Llama 3.2 to answer
response_llama = ollama.chat(model=MODEL_LLAMA, messages=messages)['message']['content']
with open("explain_llama.md", "w", encoding="utf-8") as f:
    f.write(response_llama)
print(open("explain_llama.md").read())

