# SchemeFinder

> **A 60-second Life-Event & Document Readiness Engine that matches Indian citizens to welfare schemes using deterministic rules, explains why they qualify in plain language, and generates an interactive Document Readiness Checklist flagging missing paperwork before they apply.**

---

## The Problem
Eligible citizens across India frequently miss out on central and state welfare entitlements because fragmented portals and confusing paperwork block them at the last mile. Applicants face bureaucratic rejection at Common Services Centres (CSCs) due to overlooked eligibility rules or missing supporting documentation.

## The Solution
SchemeFinder transforms civic entitlement verification through a fast, transparent, and private screening engine:
1. **5-Step HTMX Profile Wizard**: Gathers age, gender, state, occupation, life milestone, income bracket, and social category in under 60 seconds.
2. **Deterministic Eligibility Matcher**: Evaluates profiles against curated schemes with two clear tiers:
   - **Eligible Now**: 100% of hard and soft criteria met.
   - **Almost Eligible**: All hard criteria met, exactly 1 soft criterion missed (with the gap explicitly highlighted).
3. **Interactive Document Readiness Checklist**: Users tick paperwork they already own (Aadhaar, DBT bank passbook, income certificate), driving a live HTMX Application Readiness % bar and surfacing missing paperwork with exact "where to get it" instructions.
4. **1-Page Printable Checklist**: Formatted exclusively using pure CSS `@media print` stylesheets (zero heavy PDF generation libraries).
5. **Zero-Storage Privacy Architecture**: Stored strictly in temporary signed-cookie browser memory (`itsdangerous`). No login, no database, no analytics, no external tracking.

---

## Tech Stack & Architecture

- **Backend**: Python 3.14 + **FastAPI** + **Uvicorn**
- **Frontend Interactivity**: **HTMX** (declarative step swaps and reactive checklist updates)
- **Templating**: **Jinja2**
- **Design System**: *Civic Parchment & Forest* (High-contrast, arm's-length mobile readability, custom CSS perforated passbook borders and rubber stamps)
- **Motion**: **GSAP 3.12** (match reveal entrance and smooth meter transitions)
- **Offline / Local Guarantee**: All frontend assets (HTMX, GSAP, ScrollTrigger, Fraunces, Plus Jakarta Sans, Noto Sans Devanagari) are 100% vendored locally in `static/vendor/`. **Zero external CDN or API requests**.

---

## Quickstart & Run Instructions

### 1. Prerequisites & Environment Setup
Clone the repository and ensure Python is installed:
```bash
# Verify Python
python --version
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
Copy `.env.example` to `.env` (optional; defaults to local offline evaluation mode):
```bash
cp .env.example .env
```
Key configuration settings:
```ini
# Loaded from environment variable; dev fallback is provided for offline testing
SESSION_SECRET=your-random-session-secret-here
DEMO_MODE=true
APP_ENV=development
```

### 4. Run the Server
```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```
Open **[http://127.0.0.1:8000](http://127.0.0.1:8000)** in your browser.

---

## 3 One-Click Demo Personas (Judge Walkthrough)

The homepage features 3 one-click presets designed to demonstrate the core capabilities instantly:

1. **👩🌾 Persona 1: Rural Female Farmer (Age 35, B2 Income ₹1L–₹2.5L)**
   - **Result**: Confirmed as **Eligible Now** for **PM-KISAN Samman Nidhi** and **Atal Pension Yojana**.
   - **Key Features**: 3-bullet scheme cards (Benefit, Why You Qualify, plain-text official portal URL).
2. **🎓 Persona 2: College Student, SC Category (Age 20, B3 Income ₹2.5L–₹5L)**
   - **Result**: Confirmed as **Almost Eligible** for **Post Matric Scholarship for SC Students**.
   - **Key Features**: Amber alert box highlighting the exact missed rule: *"Missed Criterion: Family income up to Rs 2.5 lakh"*.
3. **👴 Persona 3: Senior Citizen (Age 72, B1 Income <₹1L)**
   - **Result**: Confirmed as **Eligible Now** for **Ayushman Vay Vandana (PM-JAY 70+)** and the **Old Age Pension Scheme**.

### Instant Vernacular Toggle (English ⇄ हिन्दी)
Click the **हिन्दी** button in the header at any time. All scheme titles, benefit summaries, why rationales, and document instructions instantly switch into Hindi using pre-stored JSON strings (zero runtime translation latency).

---

## Verification & Test Suites

Run the automated test suites to verify each layer:
```bash
# Slice 0: Curated scheme dataset and persona matching logic
python data/test_personas.py

# Slice 1: Base layout, session cookies, local vendor assets, and offline health
python test_slice1.py

# Slice 2: 5-Step HTMX wizard transitions and demo presets
python test_slice2.py

# Slice 3: Deterministic matcher, Eligible Now / Almost Eligible, plain-text URLs
python test_slice3.py

# Slice 4: Interactive document checklist, live HTMX % bar, and print view
python test_slice4.py
```

---

## Project Structure

```text
├── main.py                     # FastAPI application routes & endpoints
├── matcher.py                  # Deterministic eligibility engine & why-text formatter
├── session.py                  # Signed cookie session management (itsdangerous)
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (DEMO_MODE=true)
├── DESIGN.md                   # Visual specification (Civic Parchment & Forest)
├── DEMO_SCRIPT.md              # 90-second judge presentation script with [CLICK] cues
├── data/
│   ├── documents.json          # 15 standard civic documents (English & Hindi)
│   ├── schemes.seed.json       # 5 draft seed schemes
│   ├── schemes.json            # 40 curated schemes (Central + 7 States)
│   ├── test_personas.py        # Logic check for the 3 demo personas
│   └── inspect_schemes.py      # Schema verification helper
├── static/
│   ├── css/styles.css          # Design system & @media print stylesheet
│   ├── js/app.js               # Local client interactivity & GSAP hooks
│   └── vendor/                 # Offline vendored libraries (HTMX, GSAP, local fonts)
└── templates/
    ├── base.html               # Civic base layout with trust banner & EN/HI toggle
    ├── index.html              # Homepage with hero & one-click demo presets
    ├── wizard.html             # Profile wizard container
    ├── wizard_step.html        # 5-step HTMX wizard partial
    ├── results.html            # Matched scheme cards & missed criteria alerts
    ├── checklist.html          # Document readiness view + 1-page printable passbook
    └── checklist_partial.html  # Live HTMX readiness meter & document tiles
```

---

## Data Governance & Integrity Notes

> [!IMPORTANT]
> **Scheme Data is Unverified Draft Data**: All scheme entries in `data/schemes.json` are curated draft prototype data. Every entry is explicitly flagged with `"needs_review": true`, `"apply_url_verified": false`, and `"last_verified": null`. All results generated by this tool are indicative only. Real-world applicants must confirm current eligibility rules and application steps directly with authorized government portals or local Common Services Centres (CSCs).

Per project data rules:
- **Unverified Draft Schemes**: All 40 central and state welfare scheme records are draft prototype records subject to official gazette verification.
- **Zero URL Invention**: Every official apply URL is currently marked `"apply_url_verified": false` and renders in the UI strictly as non-clickable plain text with `(verify on the official portal - unverified URL)`.
- **Review Status**: Every scheme entry carries `"needs_review": true` and `"last_verified": null` pending administrative verification against live state gazette notifications.
- **Notice on Screen**: Every results page explicitly states: *"Indicative only. Confirm eligibility on the official portal."*
