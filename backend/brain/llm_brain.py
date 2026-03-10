# brain/llm_brain.py

import json
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load .env variables
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.groq.com/openai/v1"   # remove this line if using OpenAI
)

SYSTEM_PROMPT = """
You are the reasoning brain of an AI desktop agent named Fury.

Convert the user command into structured JSON tasks.

Supported intents:

open_app
type_text
create_file
generate_code
run_terminal
open_website
web_search
click_text

Return ONLY a JSON list.

Example:

User: open youtube and search lo fi music

[
 {"intent":"open_website","url":"https://www.youtube.com"},
 {"intent":"web_search","site":"youtube","query":"lo fi music"}
]
"""


def interpret_with_llm(command):

    try:

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",   # good Groq model
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": command}
            ]
        )

        text = response.choices[0].message.content

        tasks = json.loads(text)

        return tasks

    except Exception as e:

        print("LLM interpretation failed:", e)

        return None