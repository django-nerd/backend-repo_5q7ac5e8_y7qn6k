import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import db, create_document, get_documents
from schemas import Couple, Memory, LoveNote

app = FastAPI(title="Fauzan Love API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Fauzan & His Girlfriend — Love API is running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"

    return response

# Helper to convert ObjectId to string

def _serialize(doc):
    if not doc:
        return doc
    d = dict(doc)
    if d.get("_id"):
        d["id"] = str(d.pop("_id"))
    # Convert datetime/date fields to isoformat if present
    for k, v in list(d.items()):
        try:
            if hasattr(v, "isoformat"):
                d[k] = v.isoformat()
        except Exception:
            pass
    return d

# Public endpoints to fetch data

@app.get("/api/couple")
def get_couple_profile():
    docs = get_documents("couple", {}, limit=1)
    return _serialize(docs[0]) if docs else {}

@app.get("/api/memories")
def list_memories(limit: int = 50):
    docs = get_documents("memory", {}, limit=limit)
    return [_serialize(d) for d in docs]

@app.get("/api/notes")
def list_notes(limit: int = 50):
    docs = get_documents("lovenote", {}, limit=limit)
    return [_serialize(d) for d in docs]

# Admin endpoints to add content (simple, no auth for demo)

@app.post("/api/couple", status_code=201)
def create_couple_profile(payload: Couple):
    inserted_id = create_document("couple", payload)
    return {"id": inserted_id}

@app.post("/api/memories", status_code=201)
def create_memory(payload: Memory):
    inserted_id = create_document("memory", payload)
    return {"id": inserted_id}

@app.post("/api/notes", status_code=201)
def create_note(payload: LoveNote):
    inserted_id = create_document("lovenote", payload)
    return {"id": inserted_id}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
