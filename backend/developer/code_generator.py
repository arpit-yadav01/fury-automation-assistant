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
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You write only code"},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )

        text = response.choices[0].message.content

        if not text:
            return ""

        return text.strip()

    except Exception as e:

        print("Code gen error:", e)
        return ""