# imports

import os
import requests
import subprocess
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display
from openai import OpenAI
import ollama

# Constants
OLLAMA_API = "http://localhost:11434/api/chat"
HEADERS = {"Content-Type": "application/json"}
# MODEL = "llama3.2"

# Create a messages list using the same format that we used for OpenAI
#messages = [
#    {"role": "user", "content": "Describe some of the business applications of Generative AI"}
#]

#payload = {
#        "model": MODEL,
#        "messages": messages,
#        "stream": False
#    }

# Let's just make sure the model is loaded
# !ollama pull llama3.2 this is how to do it in Jupyter
# !ollama pull deepseek-r1:1.5b
#subprocess.run(["ollama", "pull", "llama3.2"], check=True)
subprocess.run(["ollama", "pull", "deepseek-r1:1.5b"], check=True)

# If this doesn't work for any reason, try the 2 versions in the following cells
# And double check the instructions in the 'Recap on installation of Ollama' at the top of this lab
# And if none of that works - contact me!

#response = requests.post(OLLAMA_API, json=payload, headers=HEADERS)
#print(response.json()['message']['content'])


#response = ollama.chat(model=MODEL, messages=messages)
#print(response['message']['content'])

# There's actually an alternative approach that some people might prefer
# You can use the OpenAI client python library to call Ollama:

#from openai import OpenAI //already done above
#ollama_via_openai = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')

#response = ollama_via_openai.chat.completions.create(
#    model=MODEL,
#    messages=messages
#)
#
#print(response.choices[0].message.content)

# This may take a few minutes to run! You should then see a fascinating "thinking" trace inside <think> tags, followed by some decent definitions
ollama_via_openai = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')
response = ollama_via_openai.chat.completions.create(
    model="deepseek-r1:1.5b",
    messages=[{"role": "user", "content": "Please give definitions of some core concepts behind LLMs: a neural network, attention and the transformer"}]
)

print(response.choices[0].message.content)
