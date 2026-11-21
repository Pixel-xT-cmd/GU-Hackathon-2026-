import json

with open('data/schemes.json', 'r', encoding='utf-8') as f:
    schemes = json.load(f)

print(f"Total: {len(schemes)}")
central = [s for s in schemes if s["level"] == "central"]
state = [s for s in schemes if s["level"] == "state"]
print(f"Central: {len(central)}")
print(f"State: {len(state)}")
for s in schemes:
    print(f"{s['id']:<28} | {s['level']:<7} | {s['state']:<14} | {s['category']:<26} | {s['name']}")
