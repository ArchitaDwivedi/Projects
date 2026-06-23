from typing import Optional
from dataclasses import dataclass


@dataclass
class Command:

    operation: str
    key: str
    value: Optional[str] = None
    ttl: Optional[int] = None
