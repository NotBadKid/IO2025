# python
# File: services/speech_to_text.py
import os
from typing import Optional
import speech_recognition as sr

_recognizer = sr.Recognizer()


def _pyaudio_available() -> bool:
    try:
        import pyaudio  # type: ignore
        return True
    except Exception:
        return False


def transcribe_audio_data(audio: sr.AudioData) -> str:
    """
    Transkrybuje obiekt `sr.AudioData` używając Google Web Speech API (lokalny wrapper).
    Zwraca rozpoznany tekst lub rzuca RuntimeError z komunikatem w języku polskim.
    """
    print("Audio duration (s):", len(audio.get_raw_data()) / audio.sample_rate / audio.sample_width)
    print("Sample rate:", audio.sample_rate)
    try:
        return _recognizer.recognize_google(audio, language="pl-PL")
    except sr.UnknownValueError:
        raise RuntimeError("Nie udało się rozpoznać mowy.")
    except sr.RequestError as e:
        raise RuntimeError(f"Błąd usługi rozpoznawania mowy: {e}")


def transcribe_from_microphone(timeout: Optional[float] = None, phrase_time_limit: Optional[float] = None) -> str:
    """
    Nagra krótki fragment z mikrofonu (wymaga PyAudio). Zwraca rozpoznany tekst.
    Rzuca RuntimeError jeśli PyAudio nie jest zainstalowane.
    """
    if not _pyaudio_available():
        raise RuntimeError("PyAudio nie jest zainstalowane. Zainstaluj np. `pipwin` + `pipwin install pyaudio` lub użyj pliku WAV.")
    with sr.Microphone() as source:
        _recognizer.adjust_for_ambient_noise(source)
        audio = _recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
    return transcribe_audio_data(audio)


def transcribe_file(path: str) -> str:
    """
    Transkrybuje plik WAV (ścieżka `path`). Rzuca FileNotFoundError jeśli plik nie istnieje.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    with sr.AudioFile(path) as source:
        audio = _recognizer.record(source)
    return transcribe_audio_data(audio)


def get_query(wav_path: str = "input.wav") -> str:
    """
    Wysoki poziom: próbuje mikrofon, a jeśli PyAudio nie jest dostępne lub wystąpi błąd,
    próbuje `wav_path`. Rzuca wyjątek jeśli obie metody zawiodą.
    """
    try:
        return transcribe_from_microphone()
    except Exception:
        if os.path.exists(wav_path):
            return transcribe_file(wav_path)
        raise RuntimeError("Brak dostępnego źródła audio (PyAudio nie zainstalowane i brak pliku WAV).")