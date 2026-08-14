"""
Chatbot engine: a lightweight, dependency-free rule/intent engine that
guides a website visitor through learning about Analytics Group and its
services, and can hand them off to a human via a captured lead.

Design:
- MAIN_MENU quick replies are always offered so the conversation is easy
  to navigate even for a visitor who doesn't want to type.
- Free-text input is matched against keyword sets in knowledge_base.py.
- No external LLM call is required — this keeps the bot fast, free to run,
  and 100% grounded in the company's real content (no hallucination risk).
  The engine is isolated in this module, so swapping in an LLM-backed
  implementation later only means editing this file.

Service answers:
- knowledge_base.SERVICES entries carry `name` and `summary` (required,
  used everywhere — menus, scoring) plus optional deep-dive fields:
  `definition`, `business_value`, `ag_role`, `deliverables`, `ideal_for`.
- _format_service() always leads with `summary`, then layers in whichever
  of those optional fields are present, so a service missing some of them
  still renders cleanly. Every full answer explicitly covers what the
  service is, how it helps the business, and how AG delivers it.
"""
import re
from typing import List, Tuple

from .knowledge_base import (
    COMPANY,
    SERVICES,
    GREETING_KEYWORDS,
    THANKS_KEYWORDS,
    PRICING_KEYWORDS,
    CONTACT_KEYWORDS,
    CONSULTATION_KEYWORDS,
    ABOUT_KEYWORDS,
)

QuickReply = Tuple[str, str]  # (label, payload)

MAIN_MENU: List[QuickReply] = [
    ("Our Services", "menu_services"),
    ("About Analytics Group", "menu_about"),
    ("Request a Consultation", "menu_consultation"),
    ("Contact Details", "menu_contact"),
]

SERVICE_MENU: List[QuickReply] = [(v["name"], f"service_{k}") for k, v in SERVICES.items()] + [
    ("Back to Main Menu", "menu_main")
]


def welcome_message() -> Tuple[str, List[QuickReply]]:
    text = (
        f"👋 Welcome to {COMPANY['name']}! {COMPANY['tagline']}\n\n"
        "I can tell you about our services, our track record, or connect you with our team "
        "for a consultation. What would you like to explore?"
    )
    return text, MAIN_MENU


def _service_menu_text() -> str:
    lines = ["Here's what we do — tap a service to learn more, or ask me in your own words:"]
    for s in SERVICES.values():
        lines.append(f"• {s['name']}")
    return "\n".join(lines)


def _format_service(key: str) -> Tuple[str, List[QuickReply]]:
    """
    Build the full answer for a single service.

    Always includes `name` + `summary` (guaranteed fields). Then, if
    present, layers in:
      - definition       -> what the service actually is
      - business_value   -> how it helps the business (bulleted)
      - ag_role          -> how AG specifically delivers/assists with it
      - deliverables     -> concrete outputs the client receives
    so every service answer covers "what it is", "how it helps businesses",
    and "how AG helps" in one reply, as required by the bot's brief.
    """
    service = SERVICES[key]

    parts = [f"**{service['name']}**", service["summary"]]

    definition = service.get("definition")
    if definition:
        parts.append(f"\n**What it is:**\n{definition}")

    business_value = service.get("business_value")
    if business_value:
        bullet_lines = "\n".join(f"✅ {point}" for point in business_value)
        parts.append(f"\n**How it helps your business:**\n{bullet_lines}")

    ag_role = service.get("ag_role")
    if ag_role:
        parts.append(f"\n**How Analytics Group (AG) helps:**\n{ag_role}")

    deliverables = service.get("deliverables")
    if deliverables:
        deliverable_lines = "\n".join(f"📦 {item}" for item in deliverables)
        parts.append(f"\n**What you get:**\n{deliverable_lines}")

    ideal_for = service.get("ideal_for")
    if ideal_for:
        parts.append(f"\n**Best fit for:** {ideal_for}")

    parts.append("\nWould you like to request a consultation about this, or see another service?")

    text = "\n".join(parts)

    quick_replies = [
        ("Request a Consultation", f"menu_consultation_{key}"),
        ("See Other Services", "menu_services"),
        ("Main Menu", "menu_main"),
    ]
    return text, quick_replies


def _about_text() -> str:
    stats = COMPANY["stats"]
    return (
        f"{COMPANY['about']}\n\n"
        f"📊 In numbers: {stats['happy_clients']} happy clients, {stats['projects_completed']} "
        f"completed projects, {stats['years_experience']} years of pure data experience, and "
        f"{stats['certified_specialists']} certified specialists across "
        f"{stats['certifications']}.\n\n"
        f"{COMPANY['motto']}"
    )


def _contact_text() -> str:
    c = COMPANY["contact"]
    return (
        "You can reach the Analytics Group team directly:\n\n"
        f"📍 {c['address']}\n"
        f"✉️ {c['email']}\n"
        f"📞 {c['phone']}\n"
        f"🔗 {c['linkedin']}\n\n"
        "Or, if you'd like, I can take your details now and have someone from our team "
        "reach out to you — just tap 'Request a Consultation'."
    )


def _pricing_text() -> str:
    return (
        "Great question! Pricing at Analytics Group depends on the scope of your project "
        "(data volume, systems involved, and which service — e.g. BI & Analytics, Data "
        "Science, Systems Development). Rather than guess, the best next step is a free "
        "consultation where our team can scope your needs and give you an accurate quote."
    )


def _contains_any(text: str, keywords: List[str]) -> bool:
    """
    Word-boundary aware keyword match, so short keywords like "hi" don't
    false-positive inside unrelated words like "machine".
    Multi-word keywords (e.g. "good morning") are matched as substrings
    since \\b boundaries around spaces work fine for phrases too.
    """
    for kw in keywords:
        pattern = r"\b" + re.escape(kw) + r"\b"
        if re.search(pattern, text):
            return True
    return False


def match_free_text(raw_text: str) -> Tuple[str, str, List[QuickReply]]:
    """
    Match free-typed user text to an intent.
    Returns (reply_text, intent_label, quick_replies)
    """
    text = raw_text.lower().strip()

    # 1. Greetings
    if _contains_any(text, GREETING_KEYWORDS) and len(text) < 40:
        reply, qr = welcome_message()
        return reply, "greeting", qr

    # 2. Thanks
    if _contains_any(text, THANKS_KEYWORDS):
        return (
            "You're very welcome! Anything else you'd like to know about Analytics Group?",
            "thanks",
            MAIN_MENU,
        )

    # 3. Pricing
    if _contains_any(text, PRICING_KEYWORDS):
        return _pricing_text(), "pricing", [
            ("Request a Consultation", "menu_consultation"),
            ("Main Menu", "menu_main"),
        ]

    # 4. Contact
    if _contains_any(text, CONTACT_KEYWORDS):
        return _contact_text(), "contact", MAIN_MENU

    # 5. Consultation / lead intent
    if _contains_any(text, CONSULTATION_KEYWORDS):
        return (
            "I'd love to help set that up. Could you share your name and email (and, if you "
            "like, your company and what you're interested in)? I'll pass it straight to our team.",
            "consultation_request",
            [("Main Menu", "menu_main")],
        )

    # 6. About
    if _contains_any(text, ABOUT_KEYWORDS):
        return _about_text(), "about", MAIN_MENU

    # 7. Service keyword matching — score each service by keyword hits
    best_key, best_score = None, 0
    for key, service in SERVICES.items():
        score = sum(
            1 for kw in service["keywords"] if re.search(r"\b" + re.escape(kw) + r"\b", text)
        )
        if score > best_score:
            best_key, best_score = key, score

    if best_key and best_score > 0:
        reply, qr = _format_service(best_key)
        return reply, f"service_{best_key}", qr

    # 8. Fallback
    fallback = (
        "I'm not 100% sure I caught that — I'm best at answering questions about Analytics "
        "Group's services, our track record, and putting you in touch with our team. "
        "Here's what I can help with:"
    )
    return fallback, "fallback", MAIN_MENU


def handle_payload(payload: str) -> Tuple[str, str, List[QuickReply]]:
    """Handle a structured quick-reply payload (button click)."""
    if payload == "menu_main":
        reply, qr = welcome_message()
        return reply, "menu_main", qr

    if payload == "menu_services":
        return _service_menu_text(), "menu_services", SERVICE_MENU

    if payload == "menu_about":
        return _about_text(), "menu_about", MAIN_MENU

    if payload == "menu_contact":
        return _contact_text(), "menu_contact", MAIN_MENU

    if payload.startswith("menu_consultation"):
        # may be "menu_consultation" or "menu_consultation_<service_key>"
        interest = None
        parts = payload.split("_", 2)
        if len(parts) == 3:
            interest = SERVICES.get(parts[2], {}).get("name")
        prefix = f"about **{interest}** " if interest else ""
        return (
            f"Happy to help you get {prefix}started. Please share your name and email "
            "(company and phone are optional) using the form below, and our team will "
            "be in touch shortly.",
            "menu_consultation",
            [("Main Menu", "menu_main")],
        )

    if payload.startswith("service_"):
        key = payload.replace("service_", "", 1)
        if key in SERVICES:
            return _format_service(key)

    # Unknown payload -> fall back to main menu
    reply, qr = welcome_message()
    return reply, "unknown_payload", qr
