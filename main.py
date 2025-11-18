import os
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import create_document, get_documents, db
from schemas import Service, Project, BlogPost, NewsletterSubscriber, ContactMessage, Testimonial

app = FastAPI(title="NEXORA SYNERGY API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "NEXORA SYNERGY API Running"}


@app.get("/api/hello")
def hello():
    return {"message": "Hello from the NEXORA SYNERGY backend!"}


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = getattr(db, "name", None) or "❌ Unknown"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"

    return response


# -------- Content Endpoints --------

# Seed defaults (used if DB empty). These are also used for initial frontend rendering.
DEFAULT_SERVICES: List[Service] = [
    Service(icon="Code", title="Software & Web Development", slug="software-web-development",
            summary="Custom applications, modern web platforms, and scalable architectures.", featured=True),
    Service(icon="Shield", title="Cybersecurity & Network Solutions", slug="cybersecurity-network",
            summary="Proactive defense, audits, and zero-trust strategies for resilient systems."),
    Service(icon="GitBranch", title="Digital Transformation & IT Consultancy", slug="digital-transformation",
            summary="Roadmaps, process automation, and change management for enterprise evolution."),
    Service(icon="Cloud", title="Cloud Services", slug="cloud-services",
            summary="Cloud-native design, infrastructure as code, and cost optimization."),
    Service(icon="LineChart", title="Data & Analytics", slug="data-analytics",
            summary="Dashboards, ML pipelines, and insights that move the business."),
]

DEFAULT_PROJECTS: List[Project] = [
    Project(title="Nebula Commerce Platform", slug="nebula-commerce",
            summary="Composable eCommerce with sub-second TTFB and 99.99% uptime.", tags=["Next.js", "Edge", "MongoDB"]),
    Project(title="Aegis SOC Automation", slug="aegis-soc",
            summary="SOAR workflows cutting incident response time by 68%.", tags=["Python", "SIEM", "Playbooks"]),
    Project(title="Stratus Cloud Migration", slug="stratus-migration",
            summary="Multi-cloud migration with 32% cost reduction.", tags=["Kubernetes", "IaC", "GCP/AWS"]),
]

DEFAULT_POSTS: List[BlogPost] = [
    BlogPost(title="Designing for Velocity and Safety", slug="velocity-and-safety", author="NEXORA Team",
             date=datetime.utcnow(), tags=["Architecture", "DX"],
             excerpt="How we deliver fast without compromising security.",
             content="We balance platform engineering, guardrails, and automation to ship safely."),
]


class ListResponse(BaseModel):
    items: list


@app.get("/api/content/services", response_model=ListResponse)
async def list_services():
    try:
        docs = get_documents("service")
        if docs:
            # convert ObjectId
            for d in docs:
                d["id"] = str(d.get("_id"))
                d.pop("_id", None)
            return {"items": docs}
    except Exception:
        pass
    return {"items": [s.model_dump() for s in DEFAULT_SERVICES]}


@app.get("/api/content/projects", response_model=ListResponse)
async def list_projects():
    try:
        docs = get_documents("project")
        if docs:
            for d in docs:
                d["id"] = str(d.get("_id"))
                d.pop("_id", None)
            return {"items": docs}
    except Exception:
        pass
    return {"items": [p.model_dump() for p in DEFAULT_PROJECTS]}


@app.get("/api/blog", response_model=ListResponse)
async def list_blog_posts():
    try:
        docs = get_documents("blogpost")
        if docs:
            for d in docs:
                d["id"] = str(d.get("_id"))
                d.pop("_id", None)
            return {"items": docs}
    except Exception:
        pass
    return {"items": [p.model_dump() for p in DEFAULT_POSTS]}


@app.post("/api/contact")
async def create_contact(msg: ContactMessage):
    try:
        doc_id = create_document("contactmessage", msg)
        return {"ok": True, "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/newsletter")
async def subscribe(payload: NewsletterSubscriber):
    try:
        doc_id = create_document("newslettersubscriber", payload)
        return {"ok": True, "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/testimonials", response_model=ListResponse)
async def list_testimonials():
    try:
        docs = get_documents("testimonial")
        if docs:
            for d in docs:
                d["id"] = str(d.get("_id"))
                d.pop("_id", None)
            return {"items": docs}
    except Exception:
        pass
    # Fallback sample
    sample = [
        Testimonial(name="A. Rivera", role="CTO", company="Orbit Labs",
                    quote="NEXORA accelerated our roadmap and hardened our security posture.").model_dump(),
        Testimonial(name="M. Chen", role="Head of Data", company="QuantumX",
                    quote="From pipeline reliability to dashboards, they delivered.").model_dump(),
    ]
    return {"items": sample}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
