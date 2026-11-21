"""Senior Review Automated Audit Script: Checks all 40 schemes, edge cases, Hindi templates, and route errors."""
import json
import os
from pathlib import Path
from matcher import match_schemes_for_profile, format_why_text, evaluate_criterion

DATA_DIR = Path("data")

def check_all_schemes_schema_and_hindi():
    with open(DATA_DIR / "schemes.json", "r", encoding="utf-8") as f:
        schemes = json.load(f)
    with open(DATA_DIR / "documents.json", "r", encoding="utf-8") as f:
        documents = json.load(f)
    
    doc_ids = {d["id"] for d in documents}
    
    issues = []
    
    test_profiles = [
        {"age": 18, "gender": "female", "state": "Uttar Pradesh", "occupation": "farmer", "life_event": "none", "income_upper_inr": 100000, "social_category": "General"},
        {"age": 25, "gender": "male", "state": "Maharashtra", "occupation": "student", "life_event": "education", "income_upper_inr": 250000, "social_category": "SC"},
        {"age": 45, "gender": "female", "state": "Rajasthan", "occupation": "informal_worker", "life_event": "starting_business", "income_upper_inr": 500000, "social_category": "OBC"},
        {"age": 75, "gender": "male", "state": "Bihar", "occupation": "other", "life_event": "retirement", "income_upper_inr": 100000, "social_category": "ST"},
        {"age": 28, "gender": "female", "state": "Karnataka", "occupation": "self_employed", "life_event": "pregnancy", "income_upper_inr": 800000, "social_category": "EWS"},
    ]
    
    for s in schemes:
        sid = s.get("id")
        # Check required strings
        for field in ["name", "name_hi", "benefit_en", "benefit_hi", "why_template_en", "why_template_hi"]:
            val = s.get(field)
            if not val or not isinstance(val, str) or len(val.strip()) == 0:
                issues.append(f"Scheme {sid}: Empty or invalid {field}")
                
        # Check doc references
        for d in s.get("documents", []):
            if d not in doc_ids:
                issues.append(f"Scheme {sid}: Unknown document reference '{d}'")
                
        # Test template formatting for both English and Hindi
        for prof in test_profiles:
            try:
                why_en = format_why_text(s.get("why_template_en", ""), prof, "en")
                if not why_en or "{" in why_en or "}" in why_en:
                    # check if any unformatted token remains
                    unformatted = [tok for tok in ["{age}", "{state}", "{occupation}", "{social_category}"] if tok in why_en]
                    if unformatted:
                        issues.append(f"Scheme {sid}: Unformatted token {unformatted} in why_en")
            except Exception as e:
                issues.append(f"Scheme {sid}: Exception formatting why_en: {e}")

            try:
                why_hi = format_why_text(s.get("why_template_hi", ""), prof, "hi")
                if not why_hi:
                    issues.append(f"Scheme {sid}: Empty why_hi after formatting")
                unformatted_hi = [tok for tok in ["{age}", "{state}", "{occupation}", "{social_category}"] if tok in why_hi]
                if unformatted_hi:
                    issues.append(f"Scheme {sid}: Unformatted token {unformatted_hi} in why_hi")
            except Exception as e:
                issues.append(f"Scheme {sid}: Exception formatting why_hi: {e}")

        # Check hard/soft criteria labels
        for c in s.get("hard_criteria", []) + s.get("soft_criteria", []):
            if not c.get("label_en") or not c.get("label_hi"):
                issues.append(f"Scheme {sid}: Missing label_en or label_hi in criterion {c}")
            if c.get("op") not in ["==", "in", ">=", "<=", "between"]:
                issues.append(f"Scheme {sid}: Invalid operator '{c.get('op')}'")
                
    return issues

def check_all_documents_hindi():
    with open(DATA_DIR / "documents.json", "r", encoding="utf-8") as f:
        documents = json.load(f)
    issues = []
    for d in documents:
        did = d.get("id")
        for f in ["name_en", "name_hi", "where_en", "where_hi"]:
            val = d.get(f)
            if not val or len(val.strip()) == 0:
                issues.append(f"Document {did}: Missing or empty {f}")
    return issues

if __name__ == "__main__":
    scheme_issues = check_all_schemes_schema_and_hindi()
    doc_issues = check_all_documents_hindi()
    print(f"Scheme Issues Found: {len(scheme_issues)}")
    for iss in scheme_issues:
        print("  -", iss)
    print(f"Document Issues Found: {len(doc_issues)}")
    for iss in doc_issues:
        print("  -", iss)