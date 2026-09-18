# -*- coding: utf-8 -*-
"""Validate Brave Academy remake project."""
from __future__ import annotations
import json, sys
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
errors = []
warns = []

def ok(msg): print("[OK]", msg)
def err(msg): errors.append(msg); print("[ERR]", msg)
def warn(msg): warns.append(msg); print("[WARN]", msg)

def load(n):
    return json.loads((DATA / n).read_text(encoding="utf-8"))

# Title / start
sysj = load("System.json")
title = sysj.get("gameTitle", "")
if title != "勇者學院：畢業之證":
    err(f"gameTitle={title!r}")
else:
    ok(f"gameTitle={title}")
if sysj.get("startMapId") != 1:
    err(f"startMapId={sysj.get('startMapId')}")
else:
    ok("startMapId=1")

# Switches / vars
for i, n in [(21,"序章"), (24,"G1國文"), (30,"綜合考"), (31,"一年級完成")]:
    if not sysj["switches"][i]:
        err(f"switch {i} empty")
for i in range(31, 43):
    if not sysj["variables"][i]:
        err(f"variable {i} empty")
ok("switches/variables named")

# Quiz
quiz = load("quiz/grade1.json")
qs = quiz["questions"]
if len(qs) != 60: err(f"quiz count {len(qs)}")
else: ok("60 questions")
ids = [q["id"] for q in qs]
if len(ids) != len(set(ids)): err("duplicate question ids")
texts = [q["question"] for q in qs]
if len(texts) != len(set(texts)): err("duplicate question text")
for q in qs:
    if not (0 <= q["answer"] <= 3): err(f"bad answer {q['id']}")
    if len(q["options"]) != 4: err(f"options {q['id']}")
    if not q.get("explain"): err(f"empty explain {q['id']}")
    for k in ("troopIdCorrect","troopIdWrong"):
        if k not in q: err(f"missing {k} {q['id']}")
by_t = {}
for q in qs:
    by_t.setdefault(q["teacherId"], []).append(q)
for tid in ["G1_CH","G1_MA","G1_HI","G1_GE","G1_SC","G1_MG"]:
    if len(by_t.get(tid, [])) != 10:
        err(f"{tid} has {len(by_t.get(tid,[]))} questions")
ok("quiz structure")

# Maps
mi = load("MapInfos.json")
maps = {m["id"]: m["name"] for m in mi if m}
for i in range(1, 13):
    if i not in maps: err(f"missing MapInfos {i}")
    mp = load(f"Map{i:03d}.json")
    w, h = mp["width"], mp["height"]
    for e in mp.get("events") or []:
        if not e: continue
        if not (0 <= e["x"] < w and 0 <= e["y"] < h):
            err(f"Map{i:03d} event {e['id']} out of bounds {e['x']},{e['y']}")
        for page in e["pages"]:
            for c in page["list"]:
                if c["code"] == 201:
                    # transfer [dir?, mapId, x, y, ...] OR [0, mapId, x, y, d, fade]
                    params = c["parameters"]
                    mid = params[1] if len(params) > 1 else None
                    if mid is not None and mid not in maps and mid != 0:
                        warn(f"Map{i:03d} transfer to missing map {mid}")
ok("maps 001-012 present, coords checked")

# Plugin
plug = ROOT / "js" / "plugins" / "BraveAcademyQuiz.js"
if not plug.exists(): err("missing BraveAcademyQuiz.js")
else: ok("plugin file exists")
pjs = (ROOT / "js" / "plugins.js").read_text(encoding="utf-8")
if "BraveAcademyQuiz" not in pjs: err("plugin not registered")
else: ok("plugin registered")

# Actors / items
actors = load("Actors.json")
if not any(a and a.get("name") == "雷恩" for a in actors): err("missing actor 雷恩")
else: ok("actor 雷恩")
items = load("Items.json")
for iid in (31,32,33,34,35,36,37):
    if not items[iid] or not items[iid].get("name"):
        err(f"missing item {iid}")
ok("badges/pass items")

# Troops for quiz
troops = load("Troops.json")
for tid in range(21, 34):
    if tid >= len(troops) or not troops[tid]:
        err(f"missing troop {tid}")
ok("knowledge troops 21-33")

# Enemy battler files
enemies = load("Enemies.json")
img = ROOT / "img" / "enemies"
missing_bat = []
for e in enemies:
    if not e: continue
    if e["id"] < 21 or e["id"] > 33: continue
    bn = e.get("battlerName") or ""
    if bn and not (img / f"{bn}.png").exists():
        missing_bat.append((e["id"], bn))
if missing_bat:
    warn(f"missing battler images: {missing_bat[:5]}... total {len(missing_bat)}")
else:
    ok("enemy battler images exist")

print("\n==== SUMMARY ====")
print("errors", len(errors), "warns", len(warns))
for e in errors: print(" -", e)
sys.exit(1 if errors else 0)
