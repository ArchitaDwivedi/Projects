from pypdf import PdfReader
from io import BytesIO


class PDFService:

    def extract_pages(
        self,
        source: str | bytes
    ) -> list[dict]:

        # Read either from a file path or uploaded bytes
        if isinstance(source, bytes):
            reader = PdfReader(
                BytesIO(source)
            )
        else:
            reader = PdfReader(
                source
            )

        pages = []

        for page_number, page in enumerate(
            reader.pages
        ):

            text = page.extract_text()

            if text:

                pages.append(
                    {
                        "page": page_number,
                        "text": text
                    }
                )

        return pages
