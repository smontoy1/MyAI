import os
import requests
from bs4 import BeautifulSoup
import urllib3
from openai import OpenAI
import ollama
# Uncomment this and comment out the ollama block if using OpenAI
import openai
openai.api_key = os.getenv('OPENAI_API_KEY')
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
)
summary = response['choices'][0]['message']['content']

# Suppress SSL warnings (optional, only if needed)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Website:
    def __init__(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15"
        }

        try:
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            self.content = ""
            return

        soup = BeautifulSoup(response.text, 'html.parser')

        # Join all text content together for summarization
        self.content = "\n".join([p.get_text(strip=True) for p in soup.find_all(['h1', 'h2', 'h3', 'p', 'li']) if p.get_text(strip=True)])

    def summarize(self):
        if not self.content:
            return "No content found to summarize."

        prompt = f"""
You are a helpful assistant. Summarize the following website content into clean, well-formatted Markdown. 
Use appropriate headings (like #, ##), bold text, bullet points, and links if needed.
Keep the tone professional and readable.

Website content:
\"\"\"
{self.content}
\"\"\"
"""

        # You can choose between openai or ollama depending on what you're using
        try:
            response = ollama.chat(model='llama3', messages=[{"role": "user", "content": prompt}])
            summary = response['message']['content']
        except Exception as e:
            summary = f"AI summarization failed: {e}"

        return summary


if __name__ == "__main__":
    ed = Website("https://edwarddonner.com")
    markdown_summary = ed.summarize()
    print(markdown_summary)


