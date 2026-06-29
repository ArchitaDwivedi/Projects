from ..services.rag_service import RAGService
from pydantic import BaseModel
from fastapi import APIRouter
from fastapi import UploadFile


router = APIRouter()
rag_service = RAGService()


@router.post("/upload")
async def upload_file(
    file: UploadFile
):

    if file.filename is None:
        raise ValueError(
            "Uploaded file has no filename."
        )

    contents = await file.read()

    return rag_service.index_document(
        filename=file.filename,
        contents=contents
    )
