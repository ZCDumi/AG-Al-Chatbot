"""
CRUD helpers — small, focused functions that isolate SQLAlchemy queries
from the route handlers in main.py.
"""
from __future__ import annotations

from sqlalchemy.orm import Session

from . import models, schemas


def create_session(db: Session) -> models.ChatSession:
    session = models.ChatSession()
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_session(db: Session, session_id: str) -> models.ChatSession | None:
    return db.query(models.ChatSession).filter(models.ChatSession.id == session_id).first()


def get_or_create_session(db: Session, session_id: str | None) -> models.ChatSession:
    if session_id:
        existing = get_session(db, session_id)
        if existing:
            return existing
    return create_session(db)


def add_message(
    db: Session, session_id: str, sender: str, text: str, intent: str | None = None
) -> models.ChatMessage:
    message = models.ChatMessage(
        session_id=session_id, sender=sender, text=text, intent=intent
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def get_history(db: Session, session_id: str) -> list[models.ChatMessage]:
    return (
        db.query(models.ChatMessage)
        .filter(models.ChatMessage.session_id == session_id)
        .order_by(models.ChatMessage.created_at.asc())
        .all()
    )


def create_lead(db: Session, session: models.ChatSession, lead_in: schemas.LeadCreate) -> models.Lead:
    lead = models.Lead(
        session_id=session.id,
        name=lead_in.name,
        email=lead_in.email,
        phone=lead_in.phone,
        company=lead_in.company,
        interest=lead_in.interest,
        message=lead_in.message,
    )
    db.add(lead)
    # keep the visitor's identity on the session too, for convenience
    session.visitor_name = lead_in.name
    session.visitor_email = lead_in.email
    db.commit()
    db.refresh(lead)
    return lead


def list_leads(db: Session) -> list[models.Lead]:
    return db.query(models.Lead).order_by(models.Lead.created_at.desc()).all()
