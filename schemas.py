from pydantic import BaseModel
from typing import List, Dict, Optional


class TranslationRequest(BaseModel):
    """
    Request payload for creating a translation task.

    - `text`: the source text to translate
    - `languages`: list of target languages (e.g., ["fr", "es", "de"])
    """
    text: str
    languages: List[str]


class TaskResponse(BaseModel):
    """
    Response returned immediately after creating a translation task.

    - `task_id`: unique identifier of the task
    - `status`: current task status (e.g., pending, completed)
    - `translations`: empty initially, populated once task completes
    """
    task_id: int
    status: str
    translations: Dict[str, str]


class TranslationResponse(BaseModel):
    """
    Full representation of a translation task.

    Used when fetching task details after creation.
    """
    id: int
    text: str
    languages: List[str]
    status: str
    translation: Optional[Dict[str, str]] = None
