import { useEffect, useRef, useState } from "react";
import "./ChatWidget.css";

// In dev, Vite proxies /api -> http://localhost:8000 (see vite.config.js).
// In production, set VITE_API_BASE_URL to your deployed FastAPI origin,
// and make sure that origin is added to the `allow_origins` list in
// backend/app/main.py's CORSMiddleware config.
const API_BASE = import.meta.env.VITE_API_BASE_URL || "";

const MAIN_MENU_PAYLOAD = "menu_main";
const MAIN_MENU_LABEL = "Main Menu";

const EMPTY_LEAD = { name: "", email: "", phone: "", company: "", interest: "", message: "" };

function ChatIcon() {
  return (
    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path
        d="M4 5.5C4 4.67 4.67 4 5.5 4h13c.83 0 1.5.67 1.5 1.5v10c0 .83-.67 1.5-1.5 1.5H9l-4 4v-4H5.5C4.67 16 4 15.33 4 14.5v-9Z"
        fill="currentColor"
      />
    </svg>
  );
}

function CloseIcon() {
  return (
    <svg viewBox="0 0 24 24" fill="none" width="18" height="18" xmlns="http://www.w3.org/2000/svg">
      <path d="M6 6l12 12M18 6L6 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
    </svg>
  );
}

function SendIcon() {
  return (
    <svg viewBox="0 0 24 24" fill="none" width="17" height="17" xmlns="http://www.w3.org/2000/svg">
      <path d="M4 12l16-8-6 8 6 8-16-8Z" fill="currentColor" />
    </svg>
  );
}

// Very light markdown-ish rendering: **bold** and line breaks, so backend
// replies (which use a couple of markdown bullets) look clean without a
// full markdown dependency.
function renderText(text) {
  const parts = text.split(/(\*\*[^*]+\*\*)/g);
  return parts.map((part, i) =>
    part.startsWith("**") && part.endsWith("**") ? (
      <strong key={i}>{part.slice(2, -2)}</strong>
    ) : (
      <span key={i}>{part}</span>
    )
  );
}

// The backend flags lead-capture moments via intent: "consultation_request"
// (from free-typed intent like "I want a consultation") or "menu_consultation"
// (from tapping the Request a Consultation quick reply / service card CTA).
function wantsLeadForm(intent) {
  return intent === "consultation_request" || intent === "menu_consultation";
}

export default function ChatWidget() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [quickReplies, setQuickReplies] = useState([]);
  const [input, setInput] = useState("");
  const [sessionId, setSessionId] = useState(null);
  const [isTyping, setIsTyping] = useState(false);
  const [bootstrapped, setBootstrapped] = useState(false);

  const [leadFormOpen, setLeadFormOpen] = useState(false);
  const [lead, setLead] = useState(EMPTY_LEAD);
  const [leadError, setLeadError] = useState("");
  const [leadSubmitting, setLeadSubmitting] = useState(false);

  const bodyRef = useRef(null);

  useEffect(() => {
    if (open && !bootstrapped) {
      fetch(`${API_BASE}/api/chat/start`, { method: "POST" })
        .then((r) => {
          if (!r.ok) throw new Error("bad response");
          return r.json();
        })
        .then((data) => {
          setSessionId(data.session_id);
          setMessages([{ role: "bot", text: data.reply }]);
          setQuickReplies(data.quick_replies || []);
          setBootstrapped(true);
        })
        .catch(() => {
          setMessages([
            {
              role: "bot",
              text:
                "Hi! I'm the Analytics Group assistant. (I'm having trouble reaching the " +
                "server right now — please make sure the backend is running.)",
            },
          ]);
          setBootstrapped(true);
        });
    }
  }, [open, bootstrapped]);

  useEffect(() => {
    if (bodyRef.current) {
      bodyRef.current.scrollTop = bodyRef.current.scrollHeight;
    }
  }, [messages, isTyping, leadFormOpen]);

  // displayText is what shows in the chat bubble; sendText is what actually
  // gets sent to the backend as `text` (quick replies send their payload,
  // e.g. "menu_services", while the label "Our Services" is shown instead).
  async function sendMessage(displayText, sendText) {
    const toSend = (sendText ?? displayText).trim();
    const toShow = displayText.trim();
    if (!toSend) return;

    setMessages((prev) => [...prev, { role: "user", text: toShow }]);
    setQuickReplies([]);
    setInput("");
    setIsTyping(true);

    try {
      const res = await fetch(`${API_BASE}/api/chat/message`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: sessionId, text: toSend }),
      });
      if (!res.ok) throw new Error("Request failed");
      const data = await res.json();
      setSessionId(data.session_id);
      setMessages((prev) => [...prev, { role: "bot", text: data.reply }]);

      if (wantsLeadForm(data.intent)) {
        setQuickReplies([]);
        setLeadError("");
        setLeadFormOpen(true);
      } else {
        setQuickReplies(data.quick_replies || []);
      }
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          text:
            "Sorry, I couldn't reach the server just now. Please try again, or email " +
            "insights@analyticsgroup.co.za directly.",
        },
      ]);
    } finally {
      setIsTyping(false);
    }
  }

  function handleSubmit(e) {
    e.preventDefault();
    sendMessage(input);
  }

  function updateLead(field, value) {
    setLead((prev) => ({ ...prev, [field]: value }));
  }

  function closeLeadForm(cancelled) {
    setLeadFormOpen(false);
    setLead(EMPTY_LEAD);
    setLeadError("");
    if (cancelled) {
      sendMessage(MAIN_MENU_LABEL, MAIN_MENU_PAYLOAD);
    }
  }

  async function submitLead(e) {
    e.preventDefault();
    setLeadError("");

    if (!lead.name.trim() || !lead.email.trim()) {
      setLeadError("Name and email are required.");
      return;
    }

    setLeadSubmitting(true);
    try {
      const res = await fetch(`${API_BASE}/api/leads`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: sessionId,
          name: lead.name.trim(),
          email: lead.email.trim(),
          phone: lead.phone.trim() || null,
          company: lead.company.trim() || null,
          interest: lead.interest.trim() || null,
          message: lead.message.trim() || null,
        }),
      });

      if (!res.ok) {
        let detail = "Please check your details and try again.";
        try {
          const errBody = await res.json();
          if (Array.isArray(errBody.detail) && errBody.detail[0]?.msg) {
            detail = errBody.detail[0].msg;
          } else if (typeof errBody.detail === "string") {
            detail = errBody.detail;
          }
        } catch {
          /* keep default message */
        }
        setLeadError(detail);
        setLeadSubmitting(false);
        return;
      }

      const data = await res.json();
      setLeadFormOpen(false);
      setLead(EMPTY_LEAD);
      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          text:
            `Thanks, ${data.name}! We've received your details and someone from the ` +
            `Analytics Group team will be in touch shortly at ${data.email}.`,
        },
      ]);
      sendMessage(MAIN_MENU_LABEL, MAIN_MENU_PAYLOAD);
    } catch (err) {
      setLeadError("Couldn't reach the server — please try again.");
    } finally {
      setLeadSubmitting(false);
    }
  }

  return (
    <>
      {!open && (
        <button className="cw-launcher" onClick={() => setOpen(true)} aria-label="Open chat with Analytics Group assistant">
          <ChatIcon />
          <span className="cw-dot" />
        </button>
      )}

      {open && (
        <div className="cw-panel" role="dialog" aria-label="Analytics Group chat assistant">
          <div className="cw-header">
            <div className="cw-avatar">AG</div>
            <div className="cw-header-text">
              <div className="name">Analytics Group Assistant</div>
              <div className="status">Online &middot; usually replies instantly</div>
            </div>
            <button className="cw-close" onClick={() => setOpen(false)} aria-label="Close chat">
              <CloseIcon />
            </button>
          </div>

          <div className="cw-body" ref={bodyRef}>
            {messages.map((m, i) => (
              <div className={`cw-row ${m.role}`} key={i}>
                <div className="cw-bubble">{renderText(m.text)}</div>
              </div>
            ))}
            {isTyping && (
              <div className="cw-typing" aria-label="Assistant is typing">
                <span />
                <span />
                <span />
              </div>
            )}

            {leadFormOpen && (
              <form className="cw-lead-form" onSubmit={submitLead}>
                <div className="cw-lead-title">Request a consultation</div>
                <div className="cw-lead-grid">
                  <input
                    type="text"
                    placeholder="Your name*"
                    value={lead.name}
                    onChange={(e) => updateLead("name", e.target.value)}
                    required
                  />
                  <input
                    type="email"
                    placeholder="Email*"
                    value={lead.email}
                    onChange={(e) => updateLead("email", e.target.value)}
                    required
                  />
                  <input
                    type="text"
                    placeholder="Phone (optional)"
                    value={lead.phone}
                    onChange={(e) => updateLead("phone", e.target.value)}
                  />
                  <input
                    type="text"
                    placeholder="Company (optional)"
                    value={lead.company}
                    onChange={(e) => updateLead("company", e.target.value)}
                  />
                  <input
                    type="text"
                    placeholder="What are you interested in? (optional)"
                    value={lead.interest}
                    onChange={(e) => updateLead("interest", e.target.value)}
                    className="cw-lead-full"
                  />
                  <textarea
                    placeholder="Anything else we should know? (optional)"
                    value={lead.message}
                    onChange={(e) => updateLead("message", e.target.value)}
                    className="cw-lead-full"
                    rows={2}
                  />
                </div>
                {leadError && <div className="cw-lead-error">{leadError}</div>}
                <div className="cw-lead-actions">
                  <button type="button" className="cw-lead-cancel" onClick={() => closeLeadForm(true)}>
                    Cancel
                  </button>
                  <button type="submit" className="cw-lead-submit" disabled={leadSubmitting}>
                    {leadSubmitting ? "Sending..." : "Send request"}
                  </button>
                </div>
              </form>
            )}
          </div>

          {!leadFormOpen && quickReplies.length > 0 && (
            <div className="cw-quick-replies">
              {quickReplies.map((q) => (
                <button key={q.payload} className="cw-chip" onClick={() => sendMessage(q.label, q.payload)}>
                  {q.label}
                </button>
              ))}
            </div>
          )}

          {!leadFormOpen && (
            <form className="cw-inputbar" onSubmit={handleSubmit}>
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask about our services..."
                aria-label="Type a message"
              />
              <button className="cw-send" type="submit" disabled={!input.trim()} aria-label="Send message">
                <SendIcon />
              </button>
            </form>
          )}
          <div className="cw-footer">Analytics Group &middot; insights@analyticsgroup.co.za</div>
        </div>
      )}
    </>
  );
}
