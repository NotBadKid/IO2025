from flask import Flask, request, jsonify, render_template
from services import speech_to_text, text_filter, embeddings, qdrant_db, llm_client, tts
import os
import speech_recognition as sr
import tempfile
import ffmpeg
from pydub import AudioSegment
import traceback

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    file = request.files.get("audio")
    if not file:
        return jsonify({"error": "Brak pliku audio"}), 400

    # Save the uploaded file with the correct .webm suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
        file.save(tmp.name)
        print("Saved file:", tmp.name)

    try:
        # Explicitly tell pydub the format
        audio = AudioSegment.from_file(tmp.name, format="webm")

        # Convert to mono 16 kHz PCM WAV — good for speech recognition
        wav_path = tmp.name.replace(".webm", "_converted.wav")
        audio = audio.set_frame_rate(16000).set_channels(1)
        audio.export(wav_path, format="wav")

    except Exception as e:
        return jsonify({"error": f"Error converting file: {str(e)}"}), 400

    # Now use the WAV file for speech recognition
    recognizer = sr.Recognizer()

    with sr.AudioFile(wav_path) as source:
       audio_data = recognizer.record(source)

    try:
        text = speech_to_text.transcribe_audio_data(audio_data)
    except Exception as e:
        # return jsonify({"error": f"Speech recognition error: {str(e)}"}), 500
        print("Error processing audio:", e)
        traceback.print_exc()
        return {"error": str(e)}, 500

    # # Continue with your processing pipeline...
    # print(text)
    # query_vector = embeddings.create_embedding(text)
    # print(query_vector["embedding"])
    # similar = qdrant_db.search_similar(query_vector["embedding"])

    if False:
        answer = similar
    else:
        answer = llm_client.explain_and_answer(text)
        #qdrant_db.save_entry(text, answer, query_vector['embedding'])

    audio_url = tts.text_to_speech(answer)

    return jsonify({"answer": answer, "audio_url": audio_url})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
