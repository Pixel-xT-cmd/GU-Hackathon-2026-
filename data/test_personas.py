import json

with open("data/schemes.json", "r", encoding="utf-8") as f:
    schemes = json.load(f)

def evaluate_criterion(crit, profile):
    field = crit["field"]
    op = crit["op"]
    val = crit["value"]
    p_val = profile.get(field)
    if p_val is None:
        return False
    if op == "==":
        return p_val == val
    elif op == "in":
        return p_val in val
    elif op == ">=":
        return p_val >= val
    elif op == "<=":
        return p_val <= val
    elif op == "between":
        return val[0] <= p_val <= val[1]
    return False

def match_schemes(profile):
    results = []
    for s in schemes:
        # Check state filter
        if s["level"] == "state" and s["state"] != profile.get("state"):
            continue
        
        hard_met = [evaluate_criterion(c, profile) for c in s["hard_criteria"]]
        soft_met = [evaluate_criterion(c, profile) for c in s["soft_criteria"]]
        
        all_hard = all(hard_met) if hard_met else True
        total_soft = len(soft_met)
        passed_soft = sum(soft_met)
        
        if all_hard:
            if total_soft == 0 or passed_soft == total_soft:
                results.append((s["id"], "Eligible Now", None))
            elif total_soft > 0 and (total_soft - passed_soft) == 1:
                # Find missed criterion
                missed = [s["soft_criteria"][i]["label_en"] for i, ok in enumerate(soft_met) if not ok]
                results.append((s["id"], "Almost Eligible", missed[0]))
    return results

# Persona 1: Rural female farmer, age 35, B2 income (250000)
p1 = {"age": 35, "gender": "female", "state": "Uttar Pradesh", "occupation": "farmer", "life_event": "none", "income_upper_inr": 250000, "social_category": "General"}
r1 = match_schemes(p1)
print("Persona 1 results:", [(sid, st, m) for sid, st, m in r1 if sid in ['pm-kisan', 'apy']])

# Persona 2: College student, SC category, age 20, B3 income (500000)
p2 = {"age": 20, "gender": "male", "state": "Uttar Pradesh", "occupation": "student", "life_event": "education", "income_upper_inr": 500000, "social_category": "SC"}
r2 = match_schemes(p2)
print("Persona 2 results:", [(sid, st, m) for sid, st, m in r2 if sid == 'post-matric-sc'])

# Persona 3: Senior citizen, age 72, B1 income (100000)
p3 = {"age": 72, "gender": "male", "state": "Uttar Pradesh", "occupation": "other", "life_event": "retirement", "income_upper_inr": 100000, "social_category": "General"}
r3 = match_schemes(p3)
print("Persona 3 results:", [(sid, st, m) for sid, st, m in r3 if sid in ['ayushman-vay-vandana', 'ignoaps']])
