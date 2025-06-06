from pydantic import BaseModel
from typing import List


# ----------------------------
# Note Schemas
# ----------------------------

class NoteBase(BaseModel):
    title: str
    description: str


class NoteCreate(NoteBase):
    tags: List[str]


class NoteOut(NoteBase):
    id: int
    tags: List[str]

    class Config:
        from_attributes = True


# ----------------------------
# Tag Schemas
# ----------------------------

class TagBase(BaseModel):
    name: str


class TagWithNotes(BaseModel):
    id: int
    name: str
    notes: List[NoteOut]

    class Config:
        from_attributes = True