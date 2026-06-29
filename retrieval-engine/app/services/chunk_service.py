import re


class ChunkService:

    # Split each PDF page into semantic chunks while preserving page metadata.
    def chunk_text(
        self,
        pages: list[dict],
        chunk_size: int = 500
    ) -> list[dict]:

        if chunk_size <= 0:
            raise ValueError(
                "chunk_size must be positive"
            )

        chunks = []

        for page in pages:

            # Split page into paragraphs so chunks contain complete ideas
            # instead of arbitrary word windows.
            paragraphs = self._split_paragraphs(
                page["text"]
            )

            current_chunk = []
            current_words = 0

            for paragraph in paragraphs:

                paragraph_words = len(
                    paragraph.split()
                )

                # If a paragraph alone exceeds the chunk size,
                # split it into sentence-based chunks.
                if paragraph_words > chunk_size:

                    # Save any partially built chunk before handling
                    # the oversized paragraph.
                    if current_chunk:

                        chunks.append(
                            {
                                "page": page["page"],
                                "text": "\n\n".join(
                                    current_chunk
                                )
                            }
                        )

                        current_chunk = []
                        current_words = 0

                    chunks.extend(
                        self._chunk_large_paragraph(
                            paragraph,
                            page["page"],
                            chunk_size
                        )
                    )

                    continue

                # Keep adding paragraphs while the chunk remains
                # within the size limit.
                if (
                    current_words + paragraph_words
                    <= chunk_size
                ):

                    current_chunk.append(
                        paragraph
                    )

                    current_words += paragraph_words

                else:

                    # Current chunk is full, so save it.
                    chunks.append(
                        {
                            "page": page["page"],
                            "text": "\n\n".join(
                                current_chunk
                            )
                        }
                    )

                    # Start the next chunk with the previous paragraph
                    # as overlap to preserve context between chunks.
                    current_chunk = [
                        current_chunk[-1],
                        paragraph
                    ]

                    current_words = (
                        len(
                            current_chunk[0].split()
                        )
                        + paragraph_words
                    )

            # Save the final chunk for this page.
            if current_chunk:

                chunks.append(
                    {
                        "page": page["page"],
                        "text": "\n\n".join(
                            current_chunk
                        )
                    }
                )

        return chunks

    # Split page text into clean paragraphs by using blank lines.
    def _split_paragraphs(
        self,
        text: str
    ) -> list[str]:

        return [
            paragraph.strip()
            for paragraph in re.split(
                r"\n\s*\n",
                text
            )
            if paragraph.strip()
        ]

    # Split a large paragraph into smaller chunks while preserving
    # sentence boundaries whenever possible.
    def _chunk_large_paragraph(
        self,
        paragraph: str,
        page: int,
        chunk_size: int
    ) -> list[dict]:

        chunks = []

        # Split paragraph into individual sentences.
        sentences = re.split(
            r"(?<=[.!?])\s+",
            paragraph
        )

        current_chunk = []
        current_words = 0

        for sentence in sentences:

            sentence_words = len(
                sentence.split()
            )

            # Flush the current chunk once adding another sentence
            # would exceed the size limit.
            if (
                current_words + sentence_words
                > chunk_size
            ):

                chunks.append(
                    {
                        "page": page,
                        "text": " ".join(
                            current_chunk
                        )
                    }
                )

                current_chunk = []
                current_words = 0

            current_chunk.append(
                sentence
            )

            current_words += sentence_words

        # Save any remaining sentences.
        if current_chunk:

            chunks.append(
                {
                    "page": page,
                    "text": " ".join(
                        current_chunk
                    )
                }
            )

        return chunks
