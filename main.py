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
if schemes_file.exists():
    with open(schemes_file, "r", encoding="utf-8") as f:
        SCHEMES = json.load(f)
elif (DATA_DIR / "schemes_central.json").exists() and (DATA_DIR / "schemes_state.json").exists():
    with open(DATA_DIR / "schemes_central.json", "r", encoding="utf-8") as f:
        c = json.load(f)
    with open(DATA_DIR / "schemes_state.json", "r", encoding="utf-8") as f:
        s = json.load(f)
    SCHEMES = c + s
    with open(schemes_file, "w", encoding="utf-8") as f:
        json.dump(SCHEMES, f, ensure_ascii=False, indent=2)
else:
    with open(DATA_DIR / "schemes.seed.json", "r", encoding="utf-8") as f:
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

    referer = request.headers.get("referer", "/")
    if request.headers.get("HX-Request"):
        response = Response(status_code=200, headers={"HX-Refresh": "true"})
    else:
        response = RedirectResponse(url=referer, status_code=303)
    set_session(response, sess, request)
    return response

@app.post("/load-persona")
async def load_persona(request: Request, persona_id: str = Form(...)):
    sess = get_session(request)
    if persona_id in DEMO_PERSONAS:
        sess["profile"] = dict(DEMO_PERSONAS[persona_id])
    
    # Per requirement: Each persona must fill the whole profile and jump directly to the review step (Step 5)
    response = RedirectResponse(url="/wizard/step/5", status_code=303)
    set_session(response, sess, request)
    return response

# Wizard Routes
@app.get("/wizard", response_class=HTMLResponse)
async def wizard_root():
    return RedirectResponse(url="/wizard/step/1", status_code=303)

@app.get("/wizard/step/{step_num}", response_class=HTMLResponse)
async def get_wizard_step(request: Request, step_num: int, return_to: Optional[str] = None):
    step = max(1, min(5, step_num))
    sess = get_session(request)
    lang = sess.get("lang", "en")
    profile = sess.get("profile", {})
    
    ctx = {
        "step": step,
        "profile": profile,
        "lang": lang,
        "session": sess,
        "return_to": return_to
    }
    
    # If HTMX partial swap request
    if request.headers.get("HX-Request"):
        return templates.TemplateResponse(
            request=request,
            name="wizard_step.html",
            context=ctx
        )
    
    # Otherwise full page render
    return templates.TemplateResponse(
        request=request,
        name="wizard.html",
        context=ctx
    )

@app.post("/wizard/step/1", response_class=HTMLResponse)
async def post_wizard_step1(
    request: Request,
    age: int = Form(...),
    gender: str = Form(...),
    return_to: Optional[str] = Form(None)
):
    sess = get_session(request)
    sess.setdefault("profile", {})
    sess["profile"]["age"] = age
    sess["profile"]["gender"] = gender
    
    next_step = 5 if return_to == "review" else 2
    ctx = {
        "step": next_step,
        "profile": sess["profile"],
        "lang": sess.get("lang", "en"),
        "session": sess
    }
    
    if request.headers.get("HX-Request"):
        response = templates.TemplateResponse(request=request, name="wizard_step.html", context=ctx)
    else:
        response = RedirectResponse(url=f"/wizard/step/{next_step}", status_code=303)
        
    set_session(response, sess, request)
    return response

@app.post("/wizard/step/2", response_class=HTMLResponse)
async def post_wizard_step2(
    request: Request,
    state: Optional[str] = Form(None),
    state_dropdown: Optional[str] = Form(None),
    return_to: Optional[str] = Form(None)
):
    chosen_state = state or state_dropdown or "Uttar Pradesh"
    sess = get_session(request)
    sess.setdefault("profile", {})
    sess["profile"]["state"] = chosen_state
    
    next_step = 5 if return_to == "review" else 3
    ctx = {
        "step": next_step,
        "profile": sess["profile"],
        "lang": sess.get("lang", "en"),
        "session": sess
    }
    
    if request.headers.get("HX-Request"):
        response = templates.TemplateResponse(request=request, name="wizard_step.html", context=ctx)
    else:
        response = RedirectResponse(url=f"/wizard/step/{next_step}", status_code=303)
        
    set_session(response, sess, request)
    return response

@app.post("/wizard/step/3", response_class=HTMLResponse)
async def post_wizard_step3(
    request: Request,
    occupation: str = Form(...),
    life_event: str = Form(...),
    return_to: Optional[str] = Form(None)
):
    sess = get_session(request)
    sess.setdefault("profile", {})
    sess["profile"]["occupation"] = occupation
    sess["profile"]["life_event"] = life_event
    
    next_step = 5 if return_to == "review" else 4
    ctx = {
        "step": next_step,
        "profile": sess["profile"],
        "lang": sess.get("lang", "en"),
        "session": sess
    }
    
    if request.headers.get("HX-Request"):
        response = templates.TemplateResponse(request=request, name="wizard_step.html", context=ctx)
    else:
        response = RedirectResponse(url=f"/wizard/step/{next_step}", status_code=303)
        
    set_session(response, sess, request)
    return response

@app.post("/wizard/step/4", response_class=HTMLResponse)
async def post_wizard_step4(
    request: Request,
    income_upper_inr: int = Form(...),
    social_category: str = Form(...),
    return_to: Optional[str] = Form(None)
):
    sess = get_session(request)
    sess.setdefault("profile", {})
    sess["profile"]["income_upper_inr"] = income_upper_inr
    sess["profile"]["social_category"] = social_category
    
    ctx = {
        "step": 5,
        "profile": sess["profile"],
        "lang": sess.get("lang", "en"),
        "session": sess
    }
    
    if request.headers.get("HX-Request"):
        response = templates.TemplateResponse(request=request, name="wizard_step.html", context=ctx)
    else:
        response = RedirectResponse(url="/wizard/step/5", status_code=303)
        
    set_session(response, sess, request)
    return response

@app.get("/results", response_class=HTMLResponse)
async def results(request: Request):
    sess = get_session(request)
    profile = sess.get("profile", {})
    if not profile or "age" not in profile:
        return RedirectResponse(url="/wizard/step/1", status_code=303)
        
    lang = sess.get("lang", "en")
    eligible_now, almost_eligible = match_schemes_for_profile(SCHEMES, profile, lang)
    
    needed_docs = set()
    for s in eligible_now + almost_eligible:
        needed_docs.update(s.get("documents", []))
        
    return templates.TemplateResponse(
        request=request,
        name="results.html",
        context={
            "eligible_now": eligible_now,
            "almost_eligible": almost_eligible,
            "total_docs_needed": len(needed_docs),
            "profile": profile,
            "lang": lang,
            "session": sess
        }
    )

def build_checklist_context(sess: dict, lang: str) -> dict:
    profile = sess.get("profile", {})
    owned_docs = set(sess.get("owned_docs", []))
    eligible_now, almost_eligible = match_schemes_for_profile(SCHEMES, profile, lang)
    matched_schemes = eligible_now + almost_eligible

    docs_map = {}
    for s in matched_schemes:
        s_title = s.get("name_hi" if lang == "hi" else "name")
        for doc_id in s.get("documents", []):
            if doc_id in DOCS_BY_ID:
                if doc_id not in docs_map:
                    doc_item = dict(DOCS_BY_ID[doc_id])
                    doc_item["scheme_ids"] = []
                    doc_item["scheme_names"] = []
                    docs_map[doc_id] = doc_item
                docs_map[doc_id]["scheme_ids"].append(s["id"])
                if s_title not in docs_map[doc_id]["scheme_names"]:
                    docs_map[doc_id]["scheme_names"].append(s_title)

    documents_list = list(docs_map.values())
    total_needed = len(documents_list)
    owned_count = sum(1 for d in documents_list if d["id"] in owned_docs)
    readiness_pct = round((owned_count / total_needed) * 100) if total_needed > 0 else 100

    return {
        "matched_schemes": matched_schemes,
        "documents_list": documents_list,
        "owned_docs": list(owned_docs),
        "total_needed": total_needed,
        "owned_count": owned_count,
        "readiness_pct": readiness_pct,
        "profile": profile,
        "lang": lang,
        "session": sess,
        "selected_scheme_id": "all"
    }

@app.get("/checklist", response_class=HTMLResponse)
async def get_checklist(request: Request):
    sess = get_session(request)
    profile = sess.get("profile", {})
    if not profile or "age" not in profile:
        return RedirectResponse(url="/wizard/step/1", status_code=303)
        
    lang = sess.get("lang", "en")
    ctx = build_checklist_context(sess, lang)
    return templates.TemplateResponse(
        request=request,
        name="checklist.html",
        context=ctx
    )

@app.post("/checklist/toggle-doc", response_class=HTMLResponse)
async def toggle_document(request: Request, doc_id: str = Form(...)):
    sess = get_session(request)
    owned = set(sess.get("owned_docs", []))
    if doc_id in owned:
        owned.remove(doc_id)
    else:
        owned.add(doc_id)
    sess["owned_docs"] = list(owned)
    
    lang = sess.get("lang", "en")
    ctx = build_checklist_context(sess, lang)
    
    if request.headers.get("HX-Request"):
        response = templates.TemplateResponse(
            request=request,
            name="checklist_partial.html",
            context=ctx
        )
    else:
        response = RedirectResponse(url="/checklist", status_code=303)
        
    set_session(response, sess, request)
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
