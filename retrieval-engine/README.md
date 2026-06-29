# Semantic Document Intelligence Platform

> An end-to-end Retrieval-Augmented Generation (RAG) platform that
> transforms PDF documents into an intelligent, searchable knowledge
> base using semantic embeddings, vector search, and locally hosted
> Large Language Models.

------------------------------------------------------------------------

## Overview

This project implements a complete Retrieval-Augmented Generation (RAG)
pipeline from scratch using Python. Rather than relying on frameworks
that abstract away the retrieval pipeline, each stage---from document
ingestion to semantic retrieval and grounded answer generation---is
implemented as an independent service.

The system allows users to upload PDF documents, automatically indexes
them into a semantic vector space, and answers natural language
questions using only the most relevant retrieved document chunks.

The project demonstrates modern AI engineering concepts including
semantic search, vector embeddings, document versioning, modular service
design, REST APIs, and local LLM inference.

------------------------------------------------------------------------

## Features

-   Intelligent PDF ingestion
-   Duplicate & version detection using SHA-256 hashing
-   Automatic text cleaning
-   Semantic chunking with contextual overlap
-   SentenceTransformer embeddings (`all-MiniLM-L6-v2`)
-   High-performance semantic retrieval using FAISS
-   Grounded answer generation with Ollama (Llama 3.2)
-   Persistent storage of chunks, metadata and vector index
-   Automatic document replacement and re-indexing
-   FastAPI REST API

------------------------------------------------------------------------

# Architecture

``` text
                      User
                        │
        ┌───────────────┴───────────────┐
        │                               │
        ▼                               ▼
   POST /upload                   POST /ask
        │                               │
        └──────────────┬────────────────┘
                       ▼
                  FastAPI Router
                       │
                       ▼
                   RAGService
                       │
 ┌───────────┬─────────┼──────────┬────────────┐
 ▼           ▼         ▼          ▼            ▼
Hash     Registry     PDF      Chunking   Embeddings
Service   Service    Parsing      │            │
                                  ▼            ▼
                             Semantic      Vector
                              Chunks      Embeddings
                                   │
                                   ▼
                              FAISS Index
                                   │
                                   ▼
                           Retrieve Top Chunks
                                   │
                                   ▼
                               Ollama LLM
                                   │
                                   ▼
                                 Answer
```

------------------------------------------------------------------------

# Project Structure

``` text
app/
├── routers/
│   ├── upload.py
│   └── ask.py
├── services/
│   ├── rag_service.py
│   ├── pdf_service.py
│   ├── pdf_clean_service.py
│   ├── chunk_service.py
│   ├── embedding_service.py
│   ├── vector_store_service.py
│   ├── answer_service.py
│   ├── storage_service.py
│   ├── hash_service.py
│   └── document_registry_service.py
└── main.py
```

------------------------------------------------------------------------

# End-to-End Upload Pipeline

1.  User uploads a PDF.
2.  HashService generates a SHA-256 fingerprint.
3.  RegistryService checks whether the document already exists or has
    changed.
4.  PDFService extracts text page-by-page.
5.  PDFCleanService normalizes extracted text.
6.  ChunkService splits pages into semantic chunks while preserving
    context.
7.  EmbeddingService converts each chunk into a dense vector.
8.  VectorStoreService builds the FAISS index.
9.  StorageService persists the chunks, registry and index.

------------------------------------------------------------------------

# Chunking Strategy

Each page is first divided into paragraphs using blank lines.

Normal-sized paragraphs are packed into chunks of approximately 500
words.

If a paragraph exceeds the chunk limit, it is further divided using
sentence boundaries rather than arbitrary word counts to preserve
meaning.

Neighbouring chunks intentionally overlap by repeating the final
paragraph of the previous chunk. This prevents loss of context between
chunks and improves retrieval quality.

------------------------------------------------------------------------

# Retrieval Pipeline

When a user asks a question:

1.  The question is converted into an embedding.
2.  FAISS searches for the most semantically similar chunk vectors.
3.  The top matching chunks are retrieved.
4.  Those chunks are inserted into the LLM prompt.
5.  Ollama generates an answer using only the retrieved context.
6.  The answer and source pages are returned.

------------------------------------------------------------------------

# Core Services

  -----------------------------------------------------------------------
  Service                   Responsibility
  ------------------------- ---------------------------------------------
  RAGService                Orchestrates the entire workflow

  HashService               Detect duplicate or modified PDFs

  DocumentRegistryService   Track indexed documents and chunk ownership

  PDFService                Extract PDF text

  PDFCleanService           Clean extracted text

  ChunkService              Semantic chunk generation

  EmbeddingService          Generate vector embeddings

  VectorStoreService        Build and search FAISS

  StorageService            Persist metadata and index

  AnswerService             Generate grounded responses
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# API

## Upload

``` http
POST /upload
```

Indexes a new document or replaces an existing one if it has changed.

## Ask

``` http
POST /ask
Content-Type: application/json

{
  "question": "What is durability?"
}
```

Example Response

``` json
{
  "answer": "...",
  "sources": [48,52,53]
}
```

------------------------------------------------------------------------

# Tech Stack

-   Python
-   FastAPI
-   FAISS
-   Sentence Transformers
-   Ollama
-   NumPy

------------------------------------------------------------------------

# Future Improvements

-   Hybrid keyword + vector search
-   Cross-encoder reranking
-   Metadata filtering
-   Streaming responses
-   Async indexing
-   Batch embedding generation
-   Replace FAISS persistence with Qdrant or Chroma

------------------------------------------------------------------------

# Key Learnings

This project demonstrates practical experience with:

-   Retrieval-Augmented Generation (RAG)
-   Semantic search
-   Vector databases and embeddings
-   Similarity search using FAISS
-   REST API development
-   Modular backend architecture
-   Local LLM deployment
-   Document versioning and indexing strategies

------------------------------------------------------------------------

# License

This project is intended for educational and portfolio purposes.
