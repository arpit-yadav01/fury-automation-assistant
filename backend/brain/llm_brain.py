
import re
import os
from openai import OpenAI

GROQ_KEY = os.getenv("GROQ_API_KEY")

client = None

if GROQ_KEY:
    client = OpenAI(
        api_key=GROQ_KEY,
        base_url="https://api.groq.com/openai/v1"
    )


def interpret_with_llm(command):

    if client is None:
        return None

    try:

        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {
                    "role": "system",
                    "content": "Return ONLY JSON list of tasks"
                },
                {
                    "role": "user",
                    "content": command
                }
            ]
        )

        text = response.choices[0].message.content.strip()

        text = re.sub(r"```json", "", text)
        text = re.sub(r"```", "", text)

        return json.loads(text)

    except Exception:
        return None