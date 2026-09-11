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


# ---------- Staff auth ----------

class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=80)
    password: str = Field(..., min_length=1, max_length=200)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds until the token expires


class StaffUserOut(BaseModel):
    id: int
    username: str
    full_name: Optional[str] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class LeadAccessLogOut(BaseModel):
    id: int
    staff_username: str
    accessed_at: datetime
    lead_count_returned: Optional[int] = None

    class Config:
        from_attributes = True
