from fastapi import APIRouter
from pydantic import BaseModel
from app.rag.retriever import retrieve_docs
from app.services.llm_service import generate_response
from app.database.db import get_application_status
import re

router = APIRouter()

class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
def chat(request: ChatRequest):

    user_message = request.message.strip()

    # CHECK FOR APPLICATION ID (DB FIRST)
    match = re.search(r'BO\d+', user_message)

    if match:
        application_id = match.group()
        status = get_application_status(application_id)

        if status:
            return {
                "response": f"📌 Application ID {application_id} is currently '{status}'."
            }
        else:
            return {
                "response": "Invalid application ID. Please check and try again."
            }

    # OTHERWISE RUN RAG

    docs = retrieve_docs(user_message)
    context = "\n".join([doc.page_content for doc in docs])

    if not context.strip():
        return {
            "response": "I can only answer questions related to BeanOrbit International Public School."
        }

    response = generate_response(context, user_message)

    return {"response": response}
