import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_llm(prompt: str) -> str:
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Jesteś przyjaznym asystentem dla dzieci."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
