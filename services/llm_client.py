import os
from typing import Optional


def _gemini_generate(contents: str, model: str = "gemini-2.5-flash") -> str:
    try:
        from google import genai
    except Exception as e:
        raise RuntimeError("SDK Gemini niedostępne: zainstaluj `google-genai`.") from e

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Brak `GEMINI_API_KEY` w środowisku.")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model=model, contents=contents)
    return getattr(response, "text", repr(response))

def explain_and_answer(query: str) -> str:
    """
    Buduje prompt: najpierw krótkie wyjaśnienie (2 zdania), potem odpowiedź.
    Wybiera Gemini gdy jest `GEMINI_API_KEY`.
    Zwraca tekst wygenerowany przez LLM.
    """
    prompt = (
        "Proszę najpierw wyjaśnij zapytanie w dwóch krótkich zdaniach (po polsku), "
        "a następnie odpowiedz na nie.\n\n"
        f"Zapytanie: {query}"
    )

    if os.getenv("GOOGLE_AI_API_KEY"):
        return _gemini_generate(prompt)
    raise RuntimeError("Brak klucza LLM (ustaw `GEMINI_API_KEY` lub `OPENAI_API_KEY`).")