import re


class TextCleaner:

    @staticmethod
    def clean(text: str) -> str:

        text = re.sub(
            r"These materials are.*?prohibited\.",
            "",
            text,
            flags=re.DOTALL
        )

        text = re.sub(
            r"CHAPTER\s+\d+",
            "",
            text
        )

        text = re.sub(
            r"\b\d+\b",
            "",
            text
        )

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()
