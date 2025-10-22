from fastapi import FastAPI, UploadFile
from services import speech_to_text, text_filter, embeddings, qdrant_db, llm_client, tts
from models.schemas import PromptResponse

app = FastAPI(title="AI Assistant for Kids")

@app.post("/ask", response_model=PromptResponse)
async def handle_prompt(file: UploadFile):
    text = await speech_to_text.transcribe(file)

    if not text_filter.is_safe(text):
        return PromptResponse(answer="Przepraszam, nie mogę odpowiedzieć na to pytanie.", audio_url="")

    query_vector = embeddings.get_embedding(text)
    similar = qdrant_db.search_similar(query_vector)

    if similar:
        answer = similar
    else:
        answer = llm_client.ask_llm(text)

        qdrant_db.save_entry(text, answer, query_vector)

    audio_url = tts.text_to_speech(answer)

    return PromptResponse(answer=answer, audio_url=audio_url)
