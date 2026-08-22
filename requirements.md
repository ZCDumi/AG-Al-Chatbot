analytics-group-chatbot/
├── backend/
│   ├── app/            <- FastAPI app package (do not rename this folder)
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── crud.py
│   │   ├── database.py
│   │   ├── chatbot_engine.py
│   │   └── knowledge_base.py
│   └── requirements.txt
└── frontend/
    ├── index.html
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── main.jsx
        ├── App.jsx / App.css
        ├── index.css
        └── components/
            ├── ChatWidget.jsx
            └── ChatWidget.css
```

## 1. Run the backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Visit http://127.0.0.1:8000/ — you should see `{"status": "ok", ...}`.
A `chatbot.db` SQLite file is created automatically on first run.

Useful endpoints while developing:
- `GET /docs` — interactive Swagger UI for every route
- `GET /debug/tables` — inspect the SQLite schema
- `GET /api/leads` — view captured consultation requests

## 2. Run the frontend

In a **second terminal**:

```bash
cd frontend
npm install
npm run dev
```

Visit http://localhost:5173 — the site loads and the chat launcher
appears bottom-right. Vite proxies `/api/*` requests to
`http://localhost:8000` automatically (see `vite.config.js`), so no
extra configuration is needed for local development.

## 3. Deploying

When you deploy the frontend to a real domain:

1. Set `VITE_API_BASE_URL` (in a `.env` file or your host's env vars) to
   your deployed backend's URL, e.g. `VITE_API_BASE_URL=https://api.analyticsgroup.co.za`.
2. In `backend/app/main.py`, add your deployed frontend's origin to the
   `allow_origins` list in the `CORSMiddleware` config, then redeploy
   the backend. Without this step the browser will block the requests
   with a CORS error (this only matters in production — the Vite proxy
   avoids it in local dev).






