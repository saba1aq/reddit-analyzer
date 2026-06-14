from enum import StrEnum

class PostStatus(StrEnum):
    pending = "pending"
    enriching = "enriching"
    enriched = "enriched"
    failed = "failed"
