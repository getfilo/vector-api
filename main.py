from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Vector:
    def __init__(self):
        self.events = []

    def ingest(self, source, message):
        self.events.append({"source": source, "message": message})

    def decide(self):
        stats = {}

        for e in self.events:
            stats[e["source"]] = stats.get(e["source"], 0) + 1

        if not stats:
            return {"status": "NO DATA"}

        strongest = max(stats, key=stats.get)
        weakest = min(stats, key=stats.get)

        return {
            "status": "VECTOR ACTIVE",
            "strongest": strongest,
            "weakest": weakest,
            "activity": stats
        }

vector = Vector()

class Event(BaseModel):
    source: str
    message: str

@app.get("/")
def home():
    return {"message": "VECTOR API LIVE"}

@app.post("/event")
def event(e: Event):
    vector.ingest(e.source, e.message)
    return {"status": "received"}

@app.get("/decide")
def decide():
    return vector.decide()
