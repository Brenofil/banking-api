from typing import Optional
from pydantic import BaseModel


class DocumentProcessingResponse(BaseModel):
    """Response model for document processing"""

    filename: str
    size_bytes: int
    content_type: Optional[str]
    status: str
    message: str
