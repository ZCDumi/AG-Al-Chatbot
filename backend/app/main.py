"""
Analytics Group Chatbot API
============================
FastAPI backend that powers the website chatbot: guides visitors through
Analytics Group's services, answers questions, and captures consultation
requests ("leads") into SQLite via SQLAlchemy, validated with Pydantic.

Run with:
    uvicorn app.main:app --reload --port 8000
"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, crud, chatbot_engine
from .database import engine, get_db

# Create tables on startup (fine for SQLite + this project's scale;
# for production migrations, use Alembic instead).
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Analytics Group Chatbot API",
    description="Backend for the Analytics Group website chatbot.",
    version="1.0.0",
)

# Allow the React dev server (and any deployed frontend origin you add) to call this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _to_quick_reply_schema(pairs):
    return [schemas.QuickReply(label=label, payload=payload) for label, payload in pairs]


@app.get("/", tags=["health"])
def root():
    return {"status": "ok", "service": "Analytics Group Chatbot API"}
    
@app.get("/debug/tables", tags=["health"])
def debug_tables():
    """Inspect the SQLite schema — lists tables and their columns."""
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    result = {}
    for table in tables:
        columns = inspector.get_columns(table)
        result[table] = [
            {"name": col["name"], "type": str(col["type"])}
            for col in columns
        ]

    return {"tables": result}


@app.post("/api/chat/start", response_model=schemas.MessageResponse, tags=["chat"])
def start_chat(db: Session = Depends(get_db)):
    """Start a brand-new conversation and return the bot's welcome message."""
    session = crud.create_session(db)
    text, quick_replies = chatbot_engine.welcome_message()
    crud.add_message(db, session.id, sender="bot", text=text, intent="welcome")
    return schemas.MessageResponse(
        session_id=session.id,
        reply=text,
        intent="welcome",
        quick_replies=_to_quick_reply_schema(quick_replies),
    )


@app.post("/api/chat/message", response_model=schemas.MessageResponse, tags=["chat"])
def send_message(payload: schemas.MessageCreate, db: Session = Depends(get_db)):
    """
    Send a free-typed user message OR a quick-reply payload (e.g. 'menu_services').
    Creates a session automatically if session_id is not supplied.
    """
    session = crud.get_or_create_session(db, payload.session_id)

    crud.add_message(db, session.id, sender="user", text=payload.text)

    # Quick-reply button clicks are sent with a recognizable payload prefix.
    known_prefixes = ("menu_", "service_")
    if payload.text.startswith(known_prefixes):
        reply, intent, quick_replies = chatbot_engine.handle_payload(payload.text)
    else:
        reply, intent, quick_replies = chatbot_engine.match_free_text(payload.text)

    crud.add_message(db, session.id, sender="bot", text=reply, intent=intent)

    return schemas.MessageResponse(
        session_id=session.id,
        reply=reply,
        intent=intent,
        quick_replies=_to_quick_reply_schema(quick_replies),
    )


@app.get("/api/chat/{session_id}/history", response_model=schemas.ChatHistoryOut, tags=["chat"])
def chat_history(session_id: str, db: Session = Depends(get_db)):
    session = crud.get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    messages = crud.get_history(db, session_id)
    return schemas.ChatHistoryOut(session_id=session_id, messages=messages)


@app.post("/api/leads", response_model=schemas.LeadOut, tags=["leads"])
def submit_lead(lead_in: schemas.LeadCreate, db: Session = Depends(get_db)):
    """Capture a consultation request from the chatbot lead-capture form."""
    session = crud.get_or_create_session(db, lead_in.session_id)
    lead = crud.create_lead(db, session, lead_in)

    confirmation = (
            "Thanks, {lead.name}! We've received your details and someone from the "
        "Analytics Group team will be in touch shortly at " + lead.email + "."
    )
    crud.add_message(db, session.id, sender="bot", text=confirmation, intent="lead_captured")

    return lead


@app.get("/api/leads", response_model=List[schemas.LeadOut], tags=["leads"])
def get_leads(db: Session = Depends(get_db)):
    """Internal endpoint for Analytics Group staff to view captured leads."""
    return crud.list_leads(db)
