from ..services.rag_service import RAGService
from pydantic import BaseModel
from fastapi import APIRouter


router = APIRouter()

rag_service = RAGService()


class QuestionRequest(BaseModel):

    question: str


@router.post("/ask")
def ask(
    request: QuestionRequest
):
    print("ASK HIT")
    return rag_service.ask_question(
        request.question
    )
