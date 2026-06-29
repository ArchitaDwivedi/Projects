import hashlib


class HashService:

    def generate_hash(
        self,
        data: bytes
    ) -> str:

        return hashlib.sha256(
            data
        ).hexdigest()
