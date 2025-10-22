from flask import Flask, request, jsonify, render_template
from services import speech_to_text, text_filter, embeddings, qdrant_db, llm_client, tts
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "Brak pliku audio"}), 400

    text = speech_to_text.transcribe(file)



    query_vector = embeddings.create_embedding(text)
    similar = qdrant_db.search_similar(query_vector)

    if similar:
        answer = similar
    else:
        answer = llm_client.explain_and_answer(text)
        qdrant_db.save_entry(text, answer, query_vector['embedding'])

    audio_url = tts.text_to_speech(answer)

    return jsonify({"answer": answer, "audio_url": audio_url})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
