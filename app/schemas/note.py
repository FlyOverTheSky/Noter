from pydantic import BaseModel, Field

class NoteBase(BaseModel):
    title: str = Field(..., max_length=256)
    body: str = Field(..., max_length=65536)

class NoteCreate(NoteBase):
    pass

class NoteUpdate(NoteBase):
    pass

class NoteResponse(NoteBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
