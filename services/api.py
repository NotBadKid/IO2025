# python
import os
import sys
import speech_recognition as sr
from google import genai

# --- Pobranie klucza z zmiennej środowiskowej ---
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ Brak zmiennej środowiskowej `GEMINI_API_KEY`.")
    print("Ustaw ją (np. w PowerShell: [Environment]::SetEnvironmentVariable('GEMINI_API_KEY', 'TWÓJ_KLUCZ', 'User'))")
    sys.exit(1)

# --- Inicjalizacja klienta Gemini ---
client = genai.Client(api_key=api_key)

# --- Rozpoznawanie mowy z mikrofonu ---
recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("🎤 Powiedz swoje pytanie (mów teraz)...")
    recognizer.adjust_for_ambient_noise(source)  # kalibracja szumów otoczenia
    audio = recognizer.listen(source)

try:
    # rozpoznawanie mowy przy użyciu Google Speech Recognition
    query = recognizer.recognize_google(audio, language="pl-PL")
    print(f"🗣️ Rozpoznano: {query}")

    # --- Dodanie instrukcji: wyjaśnij w 2 zdaniach przed właściwym zapytaniem ---
    prompt = f"Wyjaśnij w dwóch zdaniach (po polsku): {query}"

    # --- Wysyłanie zapytania do Gemini ---
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    print("\n🤖 Odpowiedź Gemini:")
    print(getattr(response, "text", repr(response)))

except sr.UnknownValueError:
    print("❗ Nie udało się rozpoznać mowy.")
except sr.RequestError as e:
    print(f"❗ Błąd połączenia z usługą rozpoznawania mowy: {e}")