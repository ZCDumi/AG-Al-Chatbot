"""
SQLAlchemy ORM models for the Analytics Group chatbot.

Tables:
- chat_sessions: one row per visitor conversation (browser session)
- chat_messages: every message exchanged, linked to a session
- leads: contact/consultation requests captured by the chatbot
- staff_users: internal staff accounts that can log in to view leads
- lead_access_logs: audit trail of every time a staff member viewed the
  leads list (who, when, how many rows) — this is what makes access
  individually accountable instead of "anyone with the shared key"
"""
import uuid
from datetime import datetime

from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from .database import Base


def generate_uuid() -> str:
    return str(uuid.uuid4())


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(String, primary_key=True, default=generate_uuid)
    created_at = Column(DateTime, default=datetime.utcnow)
    visitor_name = Column(String, nullable=True)
    visitor_email = Column(String, nullable=True)

    messages = relationship(
        "ChatMessage", back_populates="session", cascade="all, delete-orphan"
    )
    leads = relationship(
        "Lead", back_populates="session", cascade="all, delete-orphan"
    )


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, ForeignKey("chat_sessions.id"), nullable=False)
    sender = Column(String, nullable=False)  # "user" or "bot"
    text = Column(Text, nullable=False)
    intent = Column(String, nullable=True)  # matched intent/topic, for analytics
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("ChatSession", back_populates="messages")


class Lead(Base):
    """Captured when a visitor asks for a consultation / to be contacted."""

    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, ForeignKey("chat_sessions.id"), nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    company = Column(String, nullable=True)
    interest = Column(String, nullable=True)  # which service they asked about
    message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    contacted = Column(Boolean, default=False)

    session = relationship("ChatSession", back_populates="leads")


class StaffUser(Base):
    """
    An Analytics Group staff account that can log in to the admin API.

    Passwords are never stored in plain text — only `hashed_password`
    (bcrypt) is persisted. Accounts are created via the `create_staff.py`
    CLI script, not through a public API endpoint, so account creation
    itself can't be hit by an outsider.
    """

    __tablename__ = "staff_users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False, index=True)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class LeadAccessLog(Base):
    """
    One row per successful GET /api/leads call — the audit trail.

    Lets you answer "who looked at the leads list, and when?" after the
    fact, which a shared API key can never tell you.
    """

    __tablename__ = "lead_access_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    staff_username = Column(String, nullable=False, index=True)
    accessed_at = Column(DateTime, default=datetime.utcnow)
    lead_count_returned = Column(Integer, nullable=True)
