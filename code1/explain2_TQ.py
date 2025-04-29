import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from ollama._types import ResponseError
import ollama


#----------load my api key------------------
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

if not api_key:
    print('No API key was found')
    exit()
elif not api_key.startswith("sk-proj-"):
    print("API key is found but is not in the proper format")
    exit()
else:
    print("API key found and looks good so far")

# --------------- Setup & CLI args ---------------
# parse one required positional argument: the file to examine
parser = argparse.ArgumentParser(
    description="Use GPT & Llama to examine a code file and write a markdown report."
)
parser.add_argument(
    "input_file",
    help="Path to the code file you want the LLM to examine"
)
parser.add_argument(
    "--output",
    "-o",
    default="output.md",
    help="Where to write the markdown report (default: output.md)"
)
args = parser.parse_args()

if not os.path.isfile(args.input_file):
    raise FileNotFoundError(f"No such file: {args.input_file}")

with open(args.input_file, "r", encoding="utf-8") as f:
    code_to_examine = f.read()

# --------------- Build LLM prompt ---------------
MODEL_GPT = 'gpt-4o-mini'
MODEL_LLAMA = "llama-3.2"

# Ensure the model is installed locally (else pull it)
try:
    ollama.show(MODEL_LLAMA)
except ResponseError:
    print(f"Model {MODEL_LLAMA!r} not found locally; pulling now…")
    ollama.pull(MODEL_LLAMA)

# Now that it’s present, invoke chat
llama_resp = ollama.chat(model=MODEL_LLAMA, messages=messages)
reply = llama_resp["message"]["content"]
print(reply)
messages = [
    {"role": "system", "content": (
        "You are a helpful, detailed code reviewer. "
        "When I give you some code, you should point out potential bugs, style issues, "
        "and opportunities for improvement."
    )},
    {"role": "user", "content": f"Please examine this code:\n\n```python\n{code_to_examine}\n```"}
]

# --------------- Call OpenAI GPT ---------------
client = OpenAI()  # assuming your OpenAI client init is this
stream = client.chat.completions.create(
    model="gpt-4o-mini",  # or whatever MODEL_GPT you use
    messages=messages,
    stream=True
)

# collect the streamed response
gpt_report = ""
for chunk in stream:
    gpt_report += chunk.choices[0].delta.content or ""

# strip fences if you like
gpt_report = gpt_report.replace("```", "")

# --------------- Call Llama 3.2 (optional) ---------------
llama_resp = ollama.chat(model="llama-3.2", messages=messages)
llama_report = llama_resp["message"]["content"]

# --------------- Write to Markdown & print ---------------
with open(args.output, "w", encoding="utf-8") as md:
    md.write("# GPT-4 Review\n\n")
    md.write(gpt_report.strip())
    md.write("\n\n---\n\n")
    md.write("# Llama 3.2 Review\n\n")
    md.write(llama_report.strip())

print(f"✅ Wrote combined report to {args.output}\n")
print(open(args.output, "r", encoding="utf-8").read())

