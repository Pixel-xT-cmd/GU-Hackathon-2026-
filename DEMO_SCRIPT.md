# SchemeFinder: 90-Second Demo Script

**Pitch**: A 60-second life-event and document readiness engine matching citizens to government schemes with deterministic rules, zero-storage privacy, and an interactive paperwork checklist before they apply.

---

### Timing Breakdown

| Beat | Duration | Goal |
|---|---|---|
| **Beat 1: The Last-Mile Chasm (Pain)** | 00:00 – 00:20 | Establish the problem: eligible citizens miss out not from lack of schemes, but from fragmented rules and paperwork failure. |
| **Beat 2: Deterministic Match & Bilingual Clarity (Solution)** | 00:20 – 01:10 | Demonstrate 3 distinct personas, the instant EN/HI vernacular toggle, and plain-language match rationale. |
| **Beat 3: Document Readiness & 1-Page Passbook (Result)** | 01:10 – 01:30 | Show interactive document readiness % bar updating live and the 1-page printable checklist. |

---

### Spoken Script & Presenter Action Cues

#### [00:00 – 00:20] BEAT 1: PAIN (The Last-Mile Chasm)
- **Spoken**:  
  *"Across India, citizens miss out on welfare schemes they are legally entitled to. The barrier isn’t a lack of programs—it’s the last mile: confusing criteria, unexpected document rejection at CSC kiosks, and fear of uploading personal data to unknown servers.*  
  *SchemeFinder solves this in 60 seconds with pure deterministic rules, zero logins, and complete in-session privacy."*
- **Action**:  
  Show the clean Civic Parchment & Forest homepage on screen, pointing out the header trust badge:  
  **[POINT TO]** *"Zero Storage • Session Only • No Database"*

---

#### [00:20 – 00:45] BEAT 2A: PERSONA 1 & THE HINDI MOMENT
- **Spoken**:  
  *"Let's test our first citizen: a rural female farmer, age 35, in income bracket B2."*
- **Action**:  
  **[CLICK]** `👩🌾 1. Rural Female Farmer (Age 35)` preset button.  
  *(Screen jumps directly to Step 5 Review Ledger, showing all 7 profile attributes populated).*  
  **[CLICK]** `Find Matching Schemes & Checklist →` button.  
  *(Screen smoothly animates with the GSAP reveal to the Results Page).*
- **Spoken**:  
  *"Instantly, PM-KISAN and Atal Pension Yojana are confirmed as 'Eligible Now' with 100% rule matches. Notice the 3 plain-language bullets: the exact benefit, why she qualifies, and the official portal URL in plain text so unverified links are never blind redirects.*  
  *Now watch what happens when a Village Level Entrepreneur or rural citizen needs the local language."*
- **Action**:  
  **[CLICK]** Header language toggle `हिन्दी`.  
  *(Instantly, every scheme title, why rationale, benefit bullet, and trust notice updates to pre-stored Hindi without reloading or losing state).*
- **Spoken**:  
  *"Zero external translation APIs. Instant, reliable vernacular access directly from vetted JSON."*

---

#### [00:45 – 01:10] BEAT 2B: PERSONA 2 (ALMOST ELIGIBLE) & PERSONA 3 (SENIORS)
- **Action**:  
  **[CLICK]** `SchemeFinder` logo &rarr; **[CLICK]** `🎓 2. College Student, SC (Age 20)` &rarr; **[CLICK]** `Find Matching Schemes & Checklist →`.
- **Spoken**:  
  *"Here is our college student in the SC category with household income in bracket B3. Instead of a vague rejection, SchemeFinder flags the Post Matric Scholarship as 'Almost Eligible' and explicitly highlights the exact missed criterion: 'Family income up to Rs 2.5 lakh'."*
- **Action**:  
  **[CLICK]** `SchemeFinder` logo &rarr; **[CLICK]** `👴 3. Senior Citizen (Age 72)` &rarr; **[CLICK]** `Find Matching Schemes & Checklist →`.
- **Spoken**:  
  *"For our 72-year-old senior citizen, Ayushman Vay Vandana and the Old Age Pension appear immediately as Eligible Now."*

---

#### [01:10 – 01:30] BEAT 3: RESULT (The Document Readiness Checklist)
- **Spoken**:  
  *"Knowing you qualify is only half the battle. What paperwork do you actually need before walking into a Tehsil office or kiosk?"*
- **Action**:  
  **[CLICK]** `Check Document Readiness →` button.  
  *(The Interactive Document Readiness page loads with the meter at 0%).*  
  **[CLICK]** Tick `Aadhaar card`.  
  **[CLICK]** Tick `Bank account linked for DBT`.  
  *(The live HTMX Application Readiness % bar expands to 30%, 60%, showing green checkmarks on owned documents).*
- **Spoken**:  
  *"Notice how missing documents immediately trigger actionable alerts showing exact issuing authorities—like the local Tehsil office or nearest Aadhaar centre.*  
  *Finally, citizens or VLEs can print a single-page physical readiness ledger with zero external PDF bloat."*
- **Action**:  
  **[CLICK]** `🖨️ Print 1-Page Checklist` (or press `Ctrl+P`).  
  *(Show the print preview: pure CSS `@media print` layout fitting cleanly onto one physical page with square checkboxes and the mandatory indicative disclaimer).*
- **Spoken**:  
  *"SchemeFinder: 60 seconds from confusion to a verified, document-ready application. Thank you."*
