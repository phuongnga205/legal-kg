from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ Cho phép frontend gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # hoặc ["http://localhost:5173", "http://127.0.0.1:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ask-ip")
async def ask_ip(payload: dict):
    # demo trả về
    return {
        "CASE_ID": "demo-123",
        "USER_ID": payload.get("user", {}).get("id", "unknown"),
        "SUMMARY": f"Demo answer for: {payload.get('question')}",
        "CLAUSES": [],
        "LAWYERS": []
    }
