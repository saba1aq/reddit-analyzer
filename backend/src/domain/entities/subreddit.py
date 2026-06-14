import uuid
from dataclasses import dataclass
from typing import Optional


@dataclass
class Subreddit:
    name: str
    id: Optional[uuid.UUID] = None
    enabled: bool = True
