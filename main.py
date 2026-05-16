from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# =========================
# 🧠 VECTOR CORE ENGINE
# =========================

class Vector:
    def __init__(self):
        self.events = []

    # -------------------------
    # EVENT INGESTION
    # -------------------------
    def ingest(self, source, message, priority=1):
        self.events.append({
            "source": source,
            "message": message,
            "priority": priority
        })

    # -------------------------
    # ANALYSIS ENGINE
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
                "target": weakest,
                "reason": "Low activity detected"
            })

        if score[strongest] > 10:
            actions.append({
                "type": "MAINTAIN",
                "target": strongest,
                "reason": "High performance detected"
            })

        return {
            "status": "VECTOR PHASE 2 ACTIVE",
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


# =========================
# 🧠 VECTOR INSTANCE
# =========================

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
# 🌐 API ENDPOINTS
# =========================

@app.get("/")
def home():
    return {
        "message": "VECTOR API LIVE",
        "status": "PHASE 2 ACTIVE"
    }


@app.post("/event")
def event(e: Event):
    vector.ingest(e.source, e.message, e.priority)
    return {
        "status": "event received by VECTOR"
    }


@app.get("/decide")
def decide():
    return vector.decide()


@app.post("/feedback")
def feedback(f: Feedback):
    vector.feedback(f.source, f.status)
    return {
        "status": "feedback recorded"
    }
