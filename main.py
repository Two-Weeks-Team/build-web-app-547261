import json

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from models import PlanningArtifact, SessionLocal, init_db
from routes import router


app = FastAPI(title="Build Web App API", version="1.0.0")

@app.middleware("http")
async def normalize_api_prefix(request: Request, call_next):
    if request.scope.get("path", "").startswith("/api/"):
        request.scope["path"] = request.scope["path"][4:] or "/"
    return await call_next(request)

app.include_router(router)


@app.on_event("startup")
def on_startup():
    init_db()
    db = SessionLocal()
    try:
        existing = db.query(PlanningArtifact).count()
        if existing == 0:
            seeds = [
                {
                    "title": "CampusPulse MVP Brief",
                    "raw_input": "Campus social app for live student updates and clubs.",
                    "preferences": "Audience: college students; Platform: mobile-first; Timeline: 6 weeks",
                    "summary": "CampusPulse focuses on real-time campus moments and event discovery.",
                    "items": [
                        {"section": "Problem", "content": "Students miss relevant, timely campus updates."},
                        {"section": "Target Users", "content": "Undergraduates active in clubs and campus events."}
                    ],
                    "score": 78,
                    "note": "Seeded planning playground artifact.",
                    "is_fallback": False,
                },
                {
                    "title": "Fallback Planning Draft",
                    "raw_input": "Neighborhood social discovery concept with unclear audience and scope.",
                    "preferences": "",
                    "summary": "Fallback draft narrows scope to nearby events + trusted local recommendations.",
                    "items": [
                        {"section": "MVP Scope", "content": "Event feed, local tips, and simple trust signals."},
                        {"section": "Viability Rationale", "content": "Useful utility but confidence reduced due to fuzzy segmentation."}
                    ],
                    "score": 72,
                    "note": "Generated from incomplete model extraction path.",
                    "is_fallback": True,
                },
            ]
            for s in seeds:
                db.add(
                    PlanningArtifact(
                        title=s["title"],
                        raw_input=s["raw_input"],
                        preferences_json=json.dumps({"preferences": s["preferences"]}),
                        summary=s["summary"],
                        items_json=json.dumps(s["items"]),
                        score=s["score"],
                        note=s["note"],
                        is_fallback=s["is_fallback"],
                    )
                )
            db.commit()
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
      <head>
        <title>Build Web App API</title>
        <style>
          body { background:#0b1020; color:#e8ecff; font-family:Arial,sans-serif; margin:0; padding:24px; }
          .card { background:#151b34; border:1px solid #2a335f; border-radius:12px; padding:16px; margin-bottom:16px; }
          a { color:#7db3ff; }
          code { color:#ffd48a; }
          h1,h2 { margin:0 0 10px 0; }
          ul { margin:8px 0 0 20px; }
        </style>
      </head>
      <body>
        <div class='card'>
          <h1>Build Web App API</h1>
          <p>Turn rough product ideas into execution-ready MVP briefs in one visible pass.</p>
          <p>AI-native product-planning backend with fallback-safe generation and persistent artifact shelf.</p>
        </div>
        <div class='card'>
          <h2>Endpoints</h2>
          <ul>
            <li><code>GET /health</code></li>
            <li><code>POST /plan</code> and <code>POST /api/plan</code></li>
            <li><code>POST /insights</code> and <code>POST /api/insights</code></li>
            <li><code>GET /artifacts</code> and <code>GET /api/artifacts</code></li>
            <li><code>POST /artifacts/save</code> and <code>POST /api/artifacts/save</code></li>
          </ul>
        </div>
        <div class='card'>
          <h2>Tech Stack</h2>
          <p>FastAPI, SQLAlchemy, PostgreSQL-ready models, and DigitalOcean Serverless Inference (anthropic-claude-4.6-sonnet).</p>
          <p><a href='/docs'>Swagger Docs</a> · <a href='/redoc'>ReDoc</a></p>
        </div>
      </body>
    </html>
    """
