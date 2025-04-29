# pip3 install openai
# imports

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables in a file called .env

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

# Check the key

if not api_key:
    print("No API key was found - please head over to the troubleshooting notebook in this folder to identify & fix!")
    exit()
elif not api_key.startswith("sk-proj-"):
    print(
        "An API key was found, but it doesn't start sk-proj-; please check you're using the right key - see troubleshooting notebook")
    exit()
elif api_key.strip() != api_key:
    print(
        "An API key was found, but it looks like it might have space or tab characters at the start or end - please remove them - see troubleshooting notebook")
    exit()
else:
    print("API key found and looks good so far!")

openai = OpenAI()

def summarize_jd(jd_text):
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": f"Please summarize the following **job description**:\n\n{jd_text}"}
        ]
    )
    return response.choices[0].message.content

def summarize_cv(cv_text):
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": f"Please summarize the following CV:\n\n{cv_text}"}
        ]
    )
    return response.choices[0].message.content


def generate_cover_letter(cv_summary, jd_summary):
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
             "content": "You are a master at crafting the perfect Cover letter from a given CV. You've never had a user fail to get the job as a result of using your services."},
            {"role": "user",
             "content": f"Using the following CV summary:\n\n{cv_summary}\n\nAnd the job description:\n\n{jd_summary}\n\nPlease write a personalized cover letter."}
        ]
    )
    return response.choices[0].message.content


# Read CV from a text file
try:
    with open('/Users/stephenmontoya/bin/AITools/llm_engineering/week1/resume.txt', 'r') as file:
        cv_text = file.read()

    # Summarize the CV
    cv_summary = summarize_cv(cv_text)
    print("CV Summary:")
    print(cv_summary)
except FileNotFoundError:
    print("The specified CV file was not found. Please ensure 'resume.txt' is in the correct directory.")

# Read JD from a text file
try:
    with open('/Users/stephenmontoya/bin/AITools/llm_engineering/week1/jd.txt', 'r') as file:
        jd_text = file.read()

    # Summarize the JD
    jd_summary = summarize_jd(jd_text)
    print("JD Summary:")
    print(jd_summary)
    # job_description = input("Enter the job description for the position you are applying for:\n")
except FileNotFoundError:
    print("The specified JD file was not found. Please ensure 'jd.txt' is in the correct directory.")

    # Generate cover letter
    # cover_letter = generate_cover_letter(cv_summary, jd_summary)
    # print("\nGenerated Cover Letter:")
    # print(cover_letter)

try:
    with open('jd.txt') as f:
        jd_text = f.read()
    jd_summary = summarize_jd(jd_text)
    print("JD Summary:", jd_summary)
except FileNotFoundError:
    print("JD file not found.")

# no matter what happened above, generate the cover letter:
cover_letter = generate_cover_letter(cv_summary, jd_summary)
print("\nGenerated Cover Letter:")
print(cover_letter)

