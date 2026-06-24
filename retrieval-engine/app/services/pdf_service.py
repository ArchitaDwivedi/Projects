from pypdf import PdfReader


class PDFService:

    def extract_text(self, pdf_path: str) -> str:
        reader = PdfReader(pdf_path)

        text = ""

        for page in reader.pages:
            extracted = page.extract_text()

            if extracted:
                text += extracted + "\n"

        return text


pdf_service = PDFService()

text = pdf_service.extract_text("data/uploads/redis.pdf")

print(text[:500])
