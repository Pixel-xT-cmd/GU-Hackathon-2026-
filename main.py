"""SchemeFinder FastAPI Application."""
import os
import json
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, Request, Response, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from session import get_session, set_session, clear_session
from matcher import match_schemes_for_profile

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

# Load documents and schemes
with open(DATA_DIR / "documents.json", "r", encoding="utf-8") as f:
    DOCUMENTS = json.load(f)
DOCS_BY_ID = {d["id"]: d for d in DOCUMENTS}

schemes_file = DATA_DIR / "schemes.json"
if not schemes_file.exists():
    schemes_file = DATA_DIR / "schemes.seed.json"

with open(schemes_file, "r", encoding="utf-8") as f:
    SCHEMES = json.load(f)

app = FastAPI(
    title="SchemeFinder",
    description="60-second Life-Event & Document Readiness Engine",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Templates
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Demo Presets definitions
DEMO_PERSONAS = {
    "p1_farmer": {
        "age": 35,
        "gender": "female",
        "state": "Uttar Pradesh",
        "occupation": "farmer",
        "life_event": "none",
        "income_upper_inr": 250000,
        "social_category": "General"
    },
    "p2_student": {
        "age": 20,
        "gender": "male",
        "state": "Uttar Pradesh",
        "occupation": "student",
        "life_event": "education",
        "income_upper_inr": 500000,
        "social_category": "SC"
    },
    "p3_senior": {
        "age": 72,
        "gender": "male",
        "state": "Uttar Pradesh",
        "occupation": "other",
        "life_event": "retirement",
        "income_upper_inr": 100000,
        "social_category": "General"
    }
}

@app.get("/health")
def healthcheck():
    return {
        "status": "ok",
        "app": "SchemeFinder",
        "demo_mode": os.getenv("DEMO_MODE", "true").lower() == "true",
        "schemes_count": len(SCHEMES),
        "docs_count": len(DOCUMENTS),
        "offline_ready": True,
        "external_requests": False
    }

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    sess = get_session(request)
    lang = sess.get("lang", "en")
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "lang": lang,
            "session": sess
        }
    )

@app.post("/set-lang")
async def set_language(request: Request, lang: str = Form("en")):
    sess = get_session(request)
    sess["lang"] = "hi" if lang == "hi" else "en"
    
    # Return to the referring page or index
    referer = request.headers.get("referer", "/")
    if "/checklist" in referer:
        response = RedirectResponse(url="/checklist", status_code=303)
    elif "/results" in referer:
        response = RedirectResponse(url="/results", status_code=303)
    elif "/wizard" in referer:
        response = RedirectResponse(url="/wizard", status_code=303)
    else:
        response = RedirectResponse(url="/", status_code=303)
    set_session(response, sess)
    return response

@app.post("/load-persona")
async def load_persona(request: Request, persona_id: str = Form(...)):
    if persona_id not in DEMO_PERSONAS:
        return RedirectResponse(url="/", status_code=303)
    
    sess = get_session(request)
    sess["profile"] = dict(DEMO_PERSONAS[persona_id])
    sess["owned_docs"] = []  # reset owned docs for clean state
    
    response = RedirectResponse(url="/results", status_code=303)
    set_session(response, sess)
    return response

@app.get("/wizard", response_class=HTMLResponse)
async def wizard_entry(request: Request):
    sess = get_session(request)
    lang = sess.get("lang", "en")
    profile = sess.get("profile", {})
    
    # Render wizard container with step 1
    return templates.TemplateResponse(
        request=request,
        name="wizard.html",
        context={
            "lang": lang,
            "step": 1,
            "profile": profile,
            "session": sess
        }
    )

@app.get("/wizard/step/{step_num}", response_class=HTMLResponse)
async def get_wizard_step(request: Request, step_num: int):
    sess = get_session(request)
    lang = sess.get("lang", "en")
    profile = sess.get("profile", {})
    
    if step_num < 1 or step_num > 5:
        step_num = 1
        
    return templates.TemplateResponse(
        request=request,
        name="wizard_step.html",
        context={
            "lang": lang,
            "step": step_num,
            "profile": profile,
            "session": sess
        }
    )

@app.post("/wizard/step/1")
async def post_wizard_step_1(
    request: Request,
    age: Optional[int] = Form(None),
    gender: Optional[str] = Form(None)
):
    sess = get_session(request)
    if "profile" not in sess:
        sess["profile"] = {}
        
    if age is not None:
        sess["profile"]["age"] = age
    if gender is not None:
        sess["profile"]["gender"] = gender
        
    lang = sess.get("lang", "en")
    ctx = {
        "lang": lang,
        "step": 2,
        "profile": sess["profile"],
        "session": sess
    }
    
    if request.headers.get("HX-Request"):
        response = templates.TemplateResponse(request=request, name="wizard_step.html", context=ctx)
        set_session(response, sess)
        return response
        
    response = RedirectResponse(url="/wizard/step/2", status_code=303)
    set_session(response, sess)
    return response

@app.post("/wizard/step/2")
async def post_wizard_step_2(
    request: Request,
    state: Optional[str] = Form(None)
):
    sess = get_session(request)
    if "profile" not in sess:
        sess["profile"] = {}
        
    if state is not None:
        sess["profile"]["state"] = state
        
    lang = sess.get("lang", "en")
    ctx = {
        "lang": lang,
        "step": 3,
        "profile": sess["profile"],
        "session": sess
    }
    
    if request.headers.get("HX-Request"):
        response = templates.TemplateResponse(request=request, name="wizard_step.html", context=ctx)
        set_session(response, sess)
        return response
        
    response = RedirectResponse(url="/wizard/step/3", status_code=303)
    set_session(response, sess)
    return response

@app.post("/wizard/step/3")
async def post_wizard_step_3(
    request: Request,
    occupation: Optional[str] = Form(None),
    life_event: Optional[str] = Form(None)
):
    sess = get_session(request)
    if "profile" not in sess:
        sess["profile"] = {}
        
    if occupation is not None:
        sess["profile"]["occupation"] = occupation
    if life_event is not None:
        sess["profile"]["life_event"] = life_event
        
    lang = sess.get("lang", "en")
    ctx = {
        "lang": lang,
        "step": 4,
        "profile": sess["profile"],
        "session": sess
    }
    
    if request.headers.get("HX-Request"):
        response = templates.TemplateResponse(request=request, name="wizard_step.html", context=ctx)
        set_session(response, sess)
        return response
        
    response = RedirectResponse(url="/wizard/step/4", status_code=303)
    set_session(response, sess)
    return response

@app.post("/wizard/step/4")
async def post_wizard_step_4(
    request: Request,
    income_upper_inr: Optional[float] = Form(None),
    social_category: Optional[str] = Form(None)
):
    sess = get_session(request)
    if "profile" not in sess:
        sess["profile"] = {}
        
    if income_upper_inr is not None:
        sess["profile"]["income_upper_inr"] = income_upper_inr
    if social_category is not None:
        sess["profile"]["social_category"] = social_category
        
    lang = sess.get("lang", "en")
    ctx = {
        "lang": lang,
        "step": 5,
        "profile": sess["profile"],
        "session": sess
    }
    
    if request.headers.get("HX-Request"):
        response = templates.TemplateResponse(request=request, name="wizard_step.html", context=ctx)
        set_session(response, sess)
        return response
        
    response = RedirectResponse(url="/wizard/step/5", status_code=303)
    set_session(response, sess)
    return response

@app.get("/results", response_class=HTMLResponse)
async def view_results(request: Request):
    sess = get_session(request)
    profile = sess.get("profile", {})
    lang = sess.get("lang", "en")
    
    # Run eligibility matcher
    eligible_now, almost_eligible = match_schemes_for_profile(SCHEMES, profile)
    
    return templates.TemplateResponse(
        request=request,
        name="results.html",
        context={
            "lang": lang,
            "profile": profile,
            "eligible_now": eligible_now,
            "almost_eligible": almost_eligible,
            "session": sess
        }
    )

@app.get("/checklist", response_class=HTMLResponse)
async def view_checklist(request: Request):
    sess = get_session(request)
    profile = sess.get("profile", {})
    lang = sess.get("lang", "en")
    owned_docs = set(sess.get("owned_docs", []))
    
    eligible_now, _ = match_schemes_for_profile(SCHEMES, profile)
    
    needed_doc_ids = set()
    for s in eligible_now:
        for d in s.get("required_docs", []):
            needed_doc_ids.add(d)
            
    if not needed_doc_ids:
        needed_doc_ids = {"aadhaar", "bank_passbook", "ration_card", "income_cert"}
        
    needed_docs = [DOCS_BY_ID[did] for did in needed_doc_ids if did in DOCS_BY_ID]
    
    owned_count = sum(1 for d in needed_docs if d["id"] in owned_docs)
    total_count = len(needed_docs)
    readiness_pct = int((owned_count / total_count * 100)) if total_count > 0 else 100
    
    return templates.TemplateResponse(
        request=request,
        name="checklist.html",
        context={
            "lang": lang,
            "needed_docs": needed_docs,
            "owned_docs": owned_docs,
            "readiness_pct": readiness_pct,
            "owned_count": owned_count,
            "total_count": total_count,
            "eligible_schemes_count": len(eligible_now),
            "session": sess
        }
    )

@app.post("/checklist/toggle")
async def toggle_doc(request: Request, doc_id: str = Form(...)):
    sess = get_session(request)
    owned = set(sess.get("owned_docs", []))
    if doc_id in owned:
        owned.remove(doc_id)
    else:
        owned.add(doc_id)
    sess["owned_docs"] = list(owned)
    
    profile = sess.get("profile", {})
    lang = sess.get("lang", "en")
    eligible_now, _ = match_schemes_for_profile(SCHEMES, profile)
    
    needed_doc_ids = set()
    for s in eligible_now:
        for d in s.get("required_docs", []):
            needed_doc_ids.add(d)
            
    if not needed_doc_ids:
        needed_doc_ids = {"aadhaar", "bank_passbook", "ration_card", "income_cert"}
        
    needed_docs = [DOCS_BY_ID[did] for did in needed_doc_ids if did in DOCS_BY_ID]
    
    owned_count = sum(1 for d in needed_docs if d["id"] in owned)
    total_count = len(needed_docs)
    readiness_pct = int((owned_count / total_count * 100)) if total_count > 0 else 100
    
    ctx = {
        "lang": lang,
        "needed_docs": needed_docs,
        "owned_docs": owned,
        "readiness_pct": readiness_pct,
        "owned_count": owned_count,
        "total_count": total_count,
        "eligible_schemes_count": len(eligible_now),
        "session": sess
    }
    
    if request.headers.get("HX-Request"):
        response = templates.TemplateResponse(
            request=request,
            name="checklist_partial.html",
            context=ctx
        )
        set_session(response, sess)
        return response
        
    response = RedirectResponse(url="/checklist", status_code=303)
    set_session(response, sess)
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
