# developer/code_generator.py

import os
from openai import OpenAI

GROQ_KEY = os.getenv("GROQ_API_KEY")

client = None

if GROQ_KEY:
    client = OpenAI(
        api_key=GROQ_KEY,
        base_url="https://api.groq.com/openai/v1"
    )


def generate_code(language, task):

    if client is None:
        print("No LLM key")
        return ""

    try:

        prompt = f"""
Write {language} code for:

{task}

Return only code.
"""

        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You write code only"},
                {"role": "user", "content": prompt},
            ]
        )

        text = response.choices[0].message.content

        return text

    except Exception as e:

        print("Code gen error:", e)

        return ""