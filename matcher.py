"""Deterministic Scheme Eligibility Matcher."""
import re
from typing import Dict, Any, List, Tuple, Optional

class SafeDict(dict):
    """Dictionary that returns empty string or key name for missing format keys."""
    def __missing__(self, key):
        return f"{{{key}}}"

def evaluate_criterion(criterion: Dict[str, Any], profile: Dict[str, Any]) -> bool:
    """Evaluates a single criterion dictionary against citizen profile."""
    field = criterion.get("field")
    op = criterion.get("op")
    target_val = criterion.get("value")
    
    if not field or field not in profile:
        return False
        
    actual_val = profile[field]
    if actual_val is None:
        return False

    if op == "==":
        return actual_val == target_val
    elif op == "in":
        if isinstance(target_val, (list, tuple, set)):
            return actual_val in target_val
        return actual_val == target_val
    elif op == ">=":
        try:
            return float(actual_val) >= float(target_val)
        except (ValueError, TypeError):
            return False
    elif op == "<=":
        try:
            return float(actual_val) <= float(target_val)
        except (ValueError, TypeError):
            return False
    elif op == "between":
        try:
            if isinstance(target_val, (list, tuple)) and len(target_val) == 2:
                return float(target_val[0]) <= float(actual_val) <= float(target_val[1])
            return False
        except (ValueError, TypeError):
            return False
            
    return False

def format_why_text(template: str, profile: Dict[str, Any], lang: str = "en") -> str:
    """Safely interpolate profile variables into why template."""
    if not template:
        return ""
        
    age = profile.get("age", "")
    state = profile.get("state", "")
    occ_raw = profile.get("occupation", "")
    occ_clean = occ_raw.replace("_", " ").title() if occ_raw else ""
    soc_cat = profile.get("social_category", "")
    
    mapping = SafeDict({
        "age": age,
        "state": state,
        "occupation": occ_clean,
        "social_category": soc_cat
    })
    
    try:
        return template.format_map(mapping)
    except Exception:
        return template

def match_schemes_for_profile(
    schemes: List[Dict[str, Any]],
    profile: Dict[str, Any],
    lang: str = "en"
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Evaluates profile against all schemes.
    Returns: (eligible_now_list, almost_eligible_list) sorted by match score.
    
    - "Eligible Now" = all hard and all soft criteria met.
    - "Almost Eligible" = all hard criteria met and exactly one soft criterion missed.
    - Match score = share of all criteria met (percentage).
    """
    user_state = profile.get("state")
    eligible_now = []
    almost_eligible = []

    for scheme in schemes:
        # State restriction check
        if scheme.get("level") == "state":
            scheme_state = scheme.get("state")
            if scheme_state and user_state and scheme_state != user_state:
                continue

        hard_criteria = scheme.get("hard_criteria", [])
        soft_criteria = scheme.get("soft_criteria", [])

        # Evaluate hard criteria
        hard_eval = [evaluate_criterion(c, profile) for c in hard_criteria]
        all_hard_met = all(hard_eval) if hard_criteria else True
        passed_hard_count = sum(hard_eval)

        # If any hard criterion failed, scheme is not eligible or almost eligible
        if not all_hard_met:
            continue

        # Evaluate soft criteria
        soft_eval = [evaluate_criterion(c, profile) for c in soft_criteria]
        total_soft = len(soft_criteria)
        passed_soft_count = sum(soft_eval)
        missed_soft_count = total_soft - passed_soft_count

        total_criteria = len(hard_criteria) + total_soft
        passed_criteria = passed_hard_count + passed_soft_count
        match_score = round((passed_criteria / total_criteria) * 100) if total_criteria > 0 else 100

        # Formatted Why text
        why_en = format_why_text(scheme.get("why_template_en", ""), profile, "en")
        why_hi = format_why_text(scheme.get("why_template_hi", ""), profile, "hi")

        scheme_card_data = dict(scheme)
        scheme_card_data["match_score"] = match_score
        scheme_card_data["formatted_why_en"] = why_en
        scheme_card_data["formatted_why_hi"] = why_hi

        if total_soft == 0 or missed_soft_count == 0:
            scheme_card_data["status"] = "Eligible Now"
            scheme_card_data["status_hi"] = "पात्रता प्रमाणित"
            scheme_card_data["missed_criterion_en"] = None
            scheme_card_data["missed_criterion_hi"] = None
            eligible_now.append(scheme_card_data)
        elif missed_soft_count == 1:
            # Find the single missed criterion
            missed_idx = [i for i, ok in enumerate(soft_eval) if not ok][0]
            missed_crit = soft_criteria[missed_idx]
            scheme_card_data["status"] = "Almost Eligible"
            scheme_card_data["status_hi"] = "लगभग पात्र"
            scheme_card_data["missed_criterion_en"] = missed_crit.get("label_en", "One criteria unmet")
            scheme_card_data["missed_criterion_hi"] = missed_crit.get("label_hi", "एक शर्त अपूर्ण")
            almost_eligible.append(scheme_card_data)

    # Sort each list by match score descending, then scheme name
    eligible_now.sort(key=lambda s: (-s["match_score"], s["name"]))
    almost_eligible.sort(key=lambda s: (-s["match_score"], s["name"]))

    return eligible_now, almost_eligible
