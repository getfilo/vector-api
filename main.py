from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Vector:
    def __init__(self):
        self.events = []

    def ingest(self, source, message):
        self.events.append({"source": source, "message": message})

    def run(self):
        stats = {}

        for e in self.events:
            stats[e["source"]] = stats.get(e["source"], 0) + 1

        if stats:
            strongest = max(stats, key=stats.get)
            weakest = min(stats, key=stats.get)
        else:
            strongest = None
            weakest = None

        return {
            "status": "VECTOR ONLINE",
            "activity": stats,
            "strongest": strongest,
            "weakest": weakest
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
    return {"status": "event received"}

@app.get("/insights")
def insights():
    return vector.run()
