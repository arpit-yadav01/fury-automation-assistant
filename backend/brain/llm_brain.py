import re
import os
import json
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
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "Return ONLY JSON list of tasks. No explanation. No markdown."
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


def generate_code(task_description):
    """Generate raw code — returns string, not JSON."""

    if client is None:
        print("LLM client not available")
        return None

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # ✅ FIXED MODEL
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a code generator. "
                        "Return ONLY raw Python code. "
                        "No explanation. No markdown. No backticks. "
                        "Just working code that runs directly."
                    )
                },
                {
                    "role": "user",
                    "content": task_description
                }
            ]
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("Code gen error:", e)
        return None