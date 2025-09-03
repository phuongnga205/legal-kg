from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import auth, qa_ip
from app.routers import lawyer
from chatbot import router as chatbot_router   # ✅ import router
from chatbot.db import init_db                 # ✅ thêm dòng này

app = FastAPI(title="Legal KG Backend")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # khi deploy đổi thành ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(auth.router, prefix="")
app.include_router(qa_ip.router, prefix="")
app.include_router(lawyer.router, prefix="/api")
app.include_router(chatbot_router.router)   # ✅ include chatbot

# ---------- Khởi tạo DB ----------
@app.on_event("startup")
def on_startup():
    init_db()
