from .hash_service import HashService
from .document_registry_service import RegistryService
from .pdf_service import PDFService
from .pdf_clean_service import TextCleaner
from .chunk_service import ChunkService
from .embedding_service import EmbeddingService
from .vector_store_service import VectorStoreService
from .answer_service import AnswerService
from .storage_service import StorageService


class RAGService:

    def __init__(self):

        self.hash_service = HashService()

        self.registry = RegistryService()

        self.pdf_service = PDFService()

        self.chunk_service = ChunkService()

        self.embedding_service = EmbeddingService()

        self.vector_store = VectorStoreService()

        self.storage_service = StorageService()

        self.answer_service = AnswerService()

        self.chunk_path = "data/indexed_chunks.json"

        self.index_path = "data/faiss.index"

    def index_document(
        self,
        filename: str,
        contents: bytes
    ) -> dict:

        # create a hash
        file_hash = self.hash_service.generate_hash(
            contents
        )

        documents = self.registry.load()

        document = self.registry.get(
            filename,
            documents
        )

        if not document:

            return self.handle_new_document(
                filename=filename,
                file_hash=file_hash,
                contents=contents,
                documents=documents
            )

        if document["hash"] == file_hash:

            return {
                "status": "exists",
                "message": "Document already indexed."
            }

        return self.replace_document(
            document=document,
            filename=filename,
            file_hash=file_hash,
            contents=contents,
            documents=documents
        )

    def build_indexed_chunks(
        self,
        contents: bytes,
        start_id: int
    ) -> list[dict]:

        pages = self.pdf_service.extract_pages(
            contents
        )

        for page in pages:

            page["text"] = TextCleaner.clean(
                page["text"]
            )

        chunks = self.chunk_service.chunk_text(
            pages
        )

        return self.embedding_service.index_chunks(
            chunks,
            start_id
        )

    def load_existing_chunks(
        self
    ) -> list[dict]:

        try:

            return self.storage_service.load(
                self.chunk_path
            )

        except FileNotFoundError:

            return []

    def remove_old_chunks(
        self,
        all_chunks: list[dict],
        vector_ids: list[int]
    ) -> list[dict]:

        return [
            chunk
            for chunk in all_chunks
            if chunk["id"] not in vector_ids
        ]

    def save_index(
        self,
        all_chunks: list[dict]
    ):

        index = self.vector_store.build_index(
            all_chunks
        )

        self.storage_service.save(
            all_chunks,
            self.chunk_path
        )

        self.vector_store.save(
            index,
            self.index_path
        )

    def replace_document(
        self,
        document: dict,
        filename: str,
        file_hash: str,
        contents: bytes,
        documents: dict
    ) -> dict:

        start_id = self.registry.get_next_vector_id(
            documents
        )

        # Create chunks for the new version
        new_chunks = self.build_indexed_chunks(
            contents,
            start_id
        )

        # Load every indexed chunk
        all_chunks = self.load_existing_chunks()

        # Remove chunks belonging to the old document
        all_chunks = self.remove_old_chunks(
            all_chunks,
            document["vector_ids"]
        )

        # Add the new version
        all_chunks.extend(
            new_chunks
        )

        # Save the updated index
        self.save_index(
            all_chunks
        )

        # Remove old registry entry
        self.registry.remove_document(
            filename,
            documents
        )

        # Add the updated registry entry
        self.registry.add_document(
            filename=filename,
            file_hash=file_hash,
            vector_ids=[
                chunk["id"]
                for chunk in new_chunks
            ],
            documents=documents
        )

        return {
            "status": "success",
            "message": "Document replaced successfully."
        }

    def handle_new_document(
        self,
        filename: str,
        file_hash: str,
        contents: bytes,
        documents: dict
    ) -> dict:

        start_id = self.registry.get_next_vector_id(
            documents
        )

        new_chunks = self.build_indexed_chunks(
            contents,
            start_id
        )

        all_chunks = self.load_existing_chunks()

        all_chunks.extend(
            new_chunks
        )

        self.save_index(
            all_chunks
        )

        self.registry.add_document(
            filename=filename,
            file_hash=file_hash,
            vector_ids=[
                chunk["id"]
                for chunk in new_chunks
            ],
            documents=documents
        )

        return {
            "status": "success",
            "message": "Document indexed successfully."
        }

    def ask_question(
        self,
        question: str
    ) -> dict:

        print("1 - loading chunks")
        indexed_chunks = self.storage_service.load(
            self.chunk_path
        )

        print("2 - loading faiss")
        index = self.vector_store.build_index(
            indexed_chunks
        )
        print(type(index))
        print(index.ntotal)
        print(index.d)

        print("3 - embedding question")
        question_embedding = self.embedding_service.generate_embedding(
            question
        )

        print(index.ntotal)
        print(index.d)
        print("4 - searching")
        matches = self.vector_store.search(
            index=index,
            query_embedding=question_embedding,
            indexed_chunks=indexed_chunks,
            k=3
        )

        print("5 - generating answer")
        answer = self.answer_service.generate_answer(
            question,
            [
                match["text"]
                for match in matches
            ]
        )

        print("6 - done")

        return {
            "answer": answer,
            "sources": sorted(
                {
                    match["page"]
                    for match in matches
                }
            )
        }
