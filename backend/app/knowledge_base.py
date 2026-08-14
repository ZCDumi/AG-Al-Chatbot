"""
Knowledge base for the Analytics Group chatbot.

Content sourced from https://analyticsgroup.co.za/ (About, Services, Stats, Contact),
expanded with fuller service definitions, business value, and AG's role in delivery.

Kept as plain Python data structures so it's easy to edit


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

# key -> service record.
# `name`, `summary`, `keywords` are REQUIRED and unchanged in shape/meaning
# from the original file — chatbot_engine.py depends on exactly these three.
# `definition`, `business_value`, `ag_role`, `deliverables`, `ideal_for` are
# NEW, additive fields for a deeper knowledge base; they are optional and
# safe to ignore for engines that don't look for them.
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
            "insights", "customer data", "kpi", "kpis", "metrics", "visualisation",
            "visualization", "power bi", "powerbi", "tableau", "qlik", "self-service reporting",
            "executive dashboard", "scorecard", "data storytelling",
        ],
        "definition": (
            "BI & Data Analytics is the practice of gathering data from across your business — "
            "sales, operations, finance, marketing, customer systems — and turning it into "
            "structured, visual, decision-ready information. It covers everything from raw data "
            "collection and cleaning, through customer segmentation and statistical modelling, "
            "to interactive dashboards that put live metrics in front of the people who need them."
        ),
        "business_value": [
            "Replaces gut-feel decisions with evidence: leaders see what's actually happening, not what they assume is happening.",
            "Segmentation reveals which customer groups are most profitable, most at risk, or most worth targeting — sharpening marketing spend.",
            "Dashboards cut the hours spent building manual spreadsheet reports every week, freeing staff for higher-value work.",
            "A single source of truth reduces disputes between departments over whose numbers are 'correct'.",
            "Faster visibility into underperforming campaigns, products, or regions means problems get caught and corrected sooner.",
        ],
        "ag_role": (
            "AG's certified BI specialists (Power BI, Tableau, Qlik) design the full pipeline: "
            "sourcing and cleaning your data, building the segmentation and statistical models "
            "behind it, and designing dashboards tailored to how your teams actually make "
            "decisions — not generic templates. AG also trains internal staff so dashboards stay "
            "useful long after the project ends, and can set up automated refreshes so reports "
            "never go stale."
        ),
        "deliverables": [
            "Customer segmentation & profiling models",
            "Interactive, tailor-made dashboards (Power BI / Tableau / Qlik)",
            "Automated recurring reporting",
            "KPI and campaign-performance tracking",
        ],
        "ideal_for": (
            "Businesses with data scattered across spreadsheets or systems that want a clear, "
            "visual, always-current view of performance."
        ),
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
            "integration", "hadoop", "spark", "pipeline", "pipelines", "data lake",
            "data warehouse", "etl", "elt", "data architecture", "real-time data",
            "streaming data", "data connectivity", "cloud data platform",
        ],
        "definition": (
            "A data fabric is an architecture that unifies data spread across many different "
            "systems — cloud, on-premise, legacy databases, third-party apps — into one "
            "consistent, accessible layer, without necessarily moving all of it into a single "
            "location. Big Data Engineering is the discipline of building the pipelines, "
            "warehouses/lakes, and infrastructure that make large volumes of data fast and "
            "reliable to work with."
        ),
        "business_value": [
            "Eliminates 'data silos' where sales, finance, and operations each have their own disconnected version of the truth.",
            "Real-time data flow means decisions can be made on what's happening now, not last month's export.",
            "Scales with the business — architecture built to handle growing data volumes without breaking.",
            "Reduces the manual, error-prone work of moving data between systems by hand.",
            "Lays the foundation that BI dashboards, data science models, and AI initiatives all depend on.",
        ],
        "ag_role": (
            "AG's data engineers design and build the pipelines and architecture that connect "
            "your systems — using tools spanning Azure, AWS, GCP, Cloudera and SQL — so data "
            "moves reliably from source to destination. AG assesses your existing landscape, "
            "identifies where silos or bottlenecks exist, and builds (or modernises) the "
            "integration layer so every other analytics initiative has clean, connected data to "
            "work from."
        ),
        "deliverables": [
            "Data pipeline design & implementation (ETL/ELT)",
            "Data lake / warehouse architecture",
            "System-to-system integration",
            "Real-time / near-real-time data flow",
        ],
        "ideal_for": (
            "Organisations whose data lives in disconnected systems and who need it flowing "
            "reliably into one place before analytics or reporting can be trusted."
        ),
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
            "security", "monitoring", "stewardship", "management", "data quality",
            "data catalog", "master data", "data policy", "access control", "audit trail",
            "popia", "gdpr", "regulatory", "data lifecycle",
        ],
        "definition": (
            "DataOps applies the automation and monitoring discipline of modern software "
            "development to data pipelines — testing, deploying, and watching data flows the "
            "same way engineering teams manage code. Data Governance is the set of policies, "
            "roles, and controls that decide who can access which data, how quality is "
            "maintained, and how the organisation stays compliant with regulations."
        ),
        "business_value": [
            "Reduces the risk of regulatory penalties by keeping data handling aligned with laws like POPIA and GDPR.",
            "Catches data quality issues (duplicates, missing values, drift) automatically instead of after a bad decision is made.",
            "Clear ownership and access rules reduce the risk of sensitive data being mishandled or leaked.",
            "Continuous monitoring means pipeline failures are caught in minutes, not discovered weeks later in a broken report.",
            "Builds trust in the numbers — stakeholders stop double-checking reports because governance already vouches for them.",
        ],
        "ag_role": (
            "AG sets up automated testing, deployment, and monitoring around your data pipelines "
            "so issues are caught before they reach decision-makers. AG also helps define "
            "practical governance policies — data ownership, access control, and quality "
            "standards — that fit your regulatory environment without slowing the business down. "
            "This includes identifying regulatory and compliance opportunities, a core part of "
            "how AG partners with clients."
        ),
        "deliverables": [
            "Automated pipeline testing & monitoring",
            "Data quality rules & alerting",
            "Access control & data ownership framework",
            "Compliance-aligned governance policy",
        ],
        "ideal_for": (
            "Businesses in regulated industries, or any organisation that has been burned by "
            "unreliable or ungoverned data before."
        ),
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
            "algorithms", "statistics", "ai", "artificial intelligence", "forecasting",
            "prediction", "churn model", "risk model", "clustering", "classification",
            "regression", "deep learning", "advanced analytics", "prescriptive analytics",
        ],
        "definition": (
            "Data science combines statistics, machine learning, and domain expertise to move "
            "beyond describing what happened (traditional BI) to predicting what's likely to "
            "happen next and recommending what to do about it. It covers predictive modelling, "
            "pattern detection, and building algorithms that learn from historical data."
        ),
        "business_value": [
            "Predictive models (e.g. churn, credit risk, fraud likelihood) let businesses act before a problem occurs, not after.",
            "Uncovers non-obvious patterns in data that human analysis alone would miss.",
            "Improves targeting and personalisation, raising conversion and retention rates.",
            "Supports smarter credit, collections, and fraud strategies — directly protecting revenue.",
            "Turns historical data into a forward-looking asset rather than just a record-keeping exercise.",
        ],
        "ag_role": (
            "AG's data scientists build and validate statistical and machine learning models "
            "tailored to your specific business problem — whether that's predicting churn, "
            "scoring credit risk, detecting fraud, or forecasting demand. AG works from your "
            "existing data (once it's clean and connected, often via the Data Fabric & "
            "Governance services) to deliver models that are interpretable and genuinely usable "
            "by business teams, not just accurate on paper."
        ),
        "deliverables": [
            "Predictive & forecasting models",
            "Customer churn / credit risk / fraud detection models",
            "Pattern & anomaly detection",
            "Model validation & performance monitoring",
        ],
        "ideal_for": (
            "Businesses that already have decent reporting in place and are ready to move from "
            "'what happened' to 'what's likely to happen next'."
        ),
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
            "caseware", "controls", "assurance", "financial audit", "audit testing",
            "audit automation", "exception testing", "data extraction audit",
            "continuous auditing", "forensic data analysis",
        ],
        "definition": (
            "Computer-Assisted Audit Techniques (CAATs) are software-driven methods auditors "
            "use to test entire populations of transactions — instead of small manual samples — "
            "to verify the accuracy, completeness, and integrity of a company's computer-based "
            "accounting and financial systems."
        ),
        "business_value": [
            "Tests 100% of transactions instead of a small sample, catching anomalies manual audits would miss.",
            "Speeds up audit cycles significantly, reducing the time finance teams spend supporting audit requests.",
            "Strengthens internal controls by surfacing exceptions, duplicates, and irregular patterns automatically.",
            "Gives management and auditors confidence in the numbers behind financial statements and regulatory filings.",
            "Supports fraud detection by flagging unusual transaction patterns for follow-up.",
        ],
        "ag_role": (
            "AG's certified specialists use industry-standard audit tools — ACL and CaseWare — "
            "to design and run CAATs against your accounting systems, extracting and testing "
            "full transaction populations rather than samples. AG builds repeatable audit "
            "routines so testing can be run continuously or at each audit cycle, and interprets "
            "the results in plain business terms for both auditors and management."
        ),
        "deliverables": [
            "Full-population transaction testing",
            "Exception and anomaly reports",
            "Repeatable/continuous audit routines",
            "Control effectiveness assessment",
        ],
        "ideal_for": (
            "Internal audit teams, external auditors, or finance leaders who need assurance "
            "over large volumes of transactional data."
        ),
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
            "development", "build a system", "upgrade", "legacy system", "modernisation",
            "modernization", "automation", "custom software", "application development",
            "web application", "internal tool", "workflow system", "digitisation",
            "digitization",
        ],
        "definition": (
            "Systems Development covers the design, build, and modernisation of the software "
            "systems a business runs on. AG addresses three common scenarios: digitising a "
            "manual, paper-based, or spreadsheet-based process; extending and upgrading an "
            "existing system that's fallen behind the business's needs; or replacing an "
            "outdated system entirely with something better fitted to purpose."
        ),
        "business_value": [
            "Removes manual, error-prone, paper-based processes that slow teams down and introduce risk.",
            "Extending an existing system is usually cheaper and less disruptive than a full replacement — AG scopes the right option rather than defaulting to a rebuild.",
            "Custom systems fit actual workflows, instead of forcing staff to work around generic off-the-shelf software.",
            "Reduces reliance on outdated or unsupported legacy systems that carry security and continuity risk.",
            "Frees staff previously doing manual data entry or reconciliation to focus on higher-value work.",
        ],
        "ag_role": (
            "AG's development team scopes which of the three paths fits your situation best — "
            "digitise, upgrade, or replace — then designs and builds the system, integrating it "
            "with your existing data and analytics infrastructure so it isn't a new silo. AG "
            "stays involved through testing and rollout so the new system is adopted smoothly, "
            "not just delivered and left behind."
        ),
        "deliverables": [
            "Custom-built business systems",
            "Legacy system upgrades & extensions",
            "Manual-to-digital process conversion",
            "System integration with existing data infrastructure",
        ],
        "ideal_for": (
            "Businesses still relying on manual processes, spreadsheets, or outdated systems "
            "that no longer scale with the business."
        ),
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

# NOTE: kept specific ("about analytics group", "who is ag") rather than the
# bare word "about" — a bare "about" would match almost any "tell me about
# <service>" question and incorrectly hijack it into the company-about
# intent before service keyword matching ever runs. Same reasoning for
# dropping the bare words "company"/"experience", which show up inside
# unrelated business questions (e.g. "our company needs a dashboard",
# "data science experience needed").
ABOUT_KEYWORDS = [
    "about analytics group", "about ag", "who are you", "what is analytics group",
    "who is ag", "who is analytics group", "your company", "your history",
    "your experience", "tell me about yourselves", "what do you do as a company",
]
