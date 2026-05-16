from fastapi import FastAPI
from pydantic import BaseModel
import threading
import time

app = FastAPI()

# =========================
# 🧠 VECTOR CORE
# =========================

class Vector:
    def __init__(self):
        self.events = []

    # -------------------------
    # INGEST DATA
    # -------------------------
    def ingest(self, source, message, priority=1):
        self.events.append({
            "source": source,
            "message": message,
            "priority": priority
        })

    # -------------------------
    # ANALYZE SYSTEM
    # -------------------------
    def analyze(self):
        score = {}

        for e in self.events:
            s = e["source"]
            score[s] = score.get(s, 0) + e["priority"]

        return score

    # -------------------------
    # DECISION ENGINE
    # -------------------------
    def decide(self):
        score = self.analyze()

        if not score:
            return {
                "status": "NO DATA",
                "message": "VECTOR has no events yet"
            }

        strongest = max(score, key=score.get)
        weakest = min(score, key=score.get)

        actions = []

        if score[weakest] < 5:
            actions.append({
                "type": "BOOST",
                "target": weakest
            })

        if score[strongest] > 10:
            actions.append({
                "type": "MAINTAIN",
                "target": strongest
            })

        return {
            "status": "VECTOR ACTIVE",
            "scores": score,
            "strongest": strongest,
            "weakest": weakest,
            "actions": actions
        }

    # -------------------------
    # FEEDBACK LOOP
    # -------------------------
    def feedback(self, source, status):
        self.events.append({
            "source": source,
            "message": f"FEEDBACK: {status}",
            "priority": 2
        })


vector = Vector()

# =========================
# 📦 REQUEST MODELS
# =========================

class Event(BaseModel):
    source: str
    message: str
    priority: int = 1


class Feedback(BaseModel):
    source: str
    status: str

# =========================
# 🌐 AUTONOMOUS THINKING
# =========================

def autonomous_loop():
    while True:
        time.sleep(10)

        score = vector.analyze()

        if not score:
            continue

        strongest = max(score, key=score.get)
        weakest = min(score, key=score.get)

        print("\n🧠 VECTOR AUTONOMOUS CYCLE")
        print("Scores:", score)
        print("Strongest:", strongest)
        print("Weakest:", weakest)

        if score[weakest] < 5:
            print("⚠️ Suggestion: BOOST", weakest)

        if score[strongest] > 10:
            print("🔥 Suggestion: MAINTAIN", strongest)

# start background brain
threading.Thread(target=autonomous_loop, daemon=True).start()

# =========================
# 🌐 API ENDPOINTS
# =========================

@app.get("/")
def home():
    return {
        "message": "VECTOR API LIVE",
        "mode": "PHASE 3 AUTONOMOUS ACTIVE"
    }


@app.post("/event")
def event(e: Event):
    vector.ingest(e.source, e.message, e.priority)
    return {"status": "event received"}


@app.get("/decide")
def decide():
    return vector.decide()


@app.post("/feedback")
def feedback(f: Feedback):
    vector.feedback(f.source, f.status)
    return {"status": "feedback recorded"}
