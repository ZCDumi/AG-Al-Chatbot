"""
Knowledge base for the Analytics Group chatbot.

Content sourced from https://analyticsgroup.co.za/ (About, Services, Stats, Contact).
Kept as plain Python data structures so it's easy to edit without touching
the matching logic in chatbot_engine.py.
"""

COMPANY = {
    "name": "Analytics Group (AG)",
    "tagline": "Talented data specialists and developers for credible, useful insights & findings.",
    "motto": '"In God we trust. All others must bring data."',
    "about": (
        "Analytics Group is a South African data analytics company. We help companies "
        "optimise profits and returns, identify regulatory and compliance opportunities, "
        "and enhance marketing, credit, fraud and collections strategies. In short, we help "
        "you understand what your data is telling you. We apply the latest analytics "
        "techniques and tools to help you generate insights, extract maximum value from your "
        "data assets, and transform your data into a perpetual source of value. Your goals "
        "are our goals — we partner with businesses to make any data-driven goal attainable."
    ),
    "stats": {
        "happy_clients": 11,
        "projects_completed": 16,
        "years_experience": 7,
        "certified_specialists": 18,
        "certifications": "Azure, AWS, GCP, Cloudera, SAP, IBM, Tableau, ACL, CaseWare, PowerBI, Qlik, SQL",
    },
    "contact": {
        "address": "332 Main Avenue, Ferndale, Randburg, Gauteng, South Africa, 2194",
        "email": "insights@analyticsgroup.co.za",
        "phone": "+27 61 468 2979",
        "linkedin": "Visit our LinkedIn Page for newsletters and updates",
        "website": "https://analyticsgroup.co.za/",
    },
}

# key -> service record. `keywords` drive the free-text intent matching.
SERVICES = {
    "bi_analytics": {
        "name": "BI & Data Analytics",
        "summary": (
            "Business Intelligence and Data Analytics is our process of collecting your data, "
            "analysing it, and turning it into clear insights you can act on — including "
            "segmentation & modelling to divide customers into targeted groups, and tailor-made "
            "dashboard reporting to present campaign metrics."
        ),
        "keywords": [
            "bi", "business intelligence", "data analytics", "analytics", "dashboard",
            "dashboards", "reporting", "reports", "segmentation", "modelling", "modeling",
            "insights", "customer data",
        ],
    },
    "data_fabric": {
        "name": "Data Fabric & Big Data Engineering",
        "summary": (
            "A data fabric gives you seamless, real-time integration and access across the "
            "many data silos of a big-data system. Our Data Fabric & Big Data Engineering "
            "service connects your data sources so information flows freely and reliably "
            "across your organisation."
        ),
        "keywords": [
            "data fabric", "big data", "engineering", "data engineering", "silos",
            "integration", "hadoop", "spark", "pipeline", "pipelines",
        ],
    },
    "data_ops_governance": {
        "name": "Data Ops & Governance",
        "summary": (
            "DataOps automation and governance run continuously as part of development, "
            "deployment, operations and monitoring — keeping your data reliable, secure, and "
            "compliant at every stage of its lifecycle."
        ),
        "keywords": [
            "dataops", "data ops", "governance", "compliance", "opsec", "data opsec",
            "security", "monitoring", "stewardship", "management",
        ],
    },
    "data_science": {
        "name": "Data Science",
        "summary": (
            "Data science is how we extract actionable insights from your raw data — using "
            "statistical modelling, machine learning and advanced analytics to uncover "
            "patterns that drive better business decisions."
        ),
        "keywords": [
            "data science", "machine learning", "ml", "predictive", "modelling",
            "algorithms", "statistics", "ai", "artificial intelligence",
        ],
    },
    "audit_caats": {
        "name": "Audit CAATs & Data Processes",
        "summary": (
            "Computer-Assisted Audit Techniques (CAATs) are used by auditors to test and "
            "conclude on the integrity of a client's computer-based accounting systems — "
            "helping you trust the numbers behind your business."
        ),
        "keywords": [
            "audit", "caats", "caat", "internal audit", "accounting system", "acl",
            "caseware", "controls", "assurance",
        ],
    },
    "systems_development": {
        "name": "Systems Development",
        "summary": (
            "We build and modernise business systems in three ways: replacing a manual "
            "system with a computerised one, upgrading and extending an existing "
            "computerised system, or replacing an existing system with a better one."
        ),
        "keywords": [
            "systems development", "software development", "system", "custom system",
            "development", "build a system", "upgrade",
        ],
    },
}

GREETING_KEYWORDS = ["hi", "hello", "hey", "howzit", "good morning", "good afternoon", "good evening"]

THANKS_KEYWORDS = ["thank", "thanks", "cheers", "appreciate"]

PRICING_KEYWORDS = ["price", "pricing", "cost", "how much", "quote", "rates", "fee", "fees"]

CONTACT_KEYWORDS = ["contact", "email", "phone", "call", "address", "location", "reach you", "get in touch"]

CONSULTATION_KEYWORDS = [
    "consultation", "consult", "talk to someone", "speak to someone", "meeting",
    "demo", "get started", "sign up", "book a call", "reach out", "connect me",
]

ABOUT_KEYWORDS = ["about", "who are you", "what is analytics group", "company", "who is ag", "history", "experience"]
