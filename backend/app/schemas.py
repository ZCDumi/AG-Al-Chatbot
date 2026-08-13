"""
Pydantic schemas: define the shape of data going in/out of the API.
"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


# ---------- Chat ----------

class MessageCreate(BaseModel):
    session_id: Optional[str] = Field(
        None, description="Existing session id. Omit to start a new conversation."
    )
    text: str = Field(..., min_length=1, max_length=1000)


class QuickReply(BaseModel):
    label: str
    payload: str


class MessageResponse(BaseModel):
    session_id: str
    reply: str
    intent: Optional[str] = None
    quick_replies: List[QuickReply] = []


class ChatMessageOut(BaseModel):
    id: int
    sender: str
    text: str
    intent: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ChatHistoryOut(BaseModel):
    session_id: str
    messages: List[ChatMessageOut]

    class Config:
        from_attributes = True


# ---------- Leads ----------

class LeadCreate(BaseModel):
    session_id: Optional[str] = None
    name: str = Field(..., min_length=1, max_length=120)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=40)
    company: Optional[str] = Field(None, max_length=120)
    interest: Optional[str] = Field(None, max_length=120)
    message: Optional[str] = Field(None, max_length=1000)


class LeadOut(BaseModel):
    id: int
    session_id: str
    name: str
    email: EmailStr
    phone: Optional[str] = None
    company: Optional[str] = None
    interest: Optional[str] = None
    message: Optional[str] = None
    created_at: datetime
    contacted: bool

    class Config:
        from_attributes = True
