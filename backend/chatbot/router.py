# -*- coding: utf-8 -*-
import os
from typing import Dict, List, Tuple
from fastapi import APIRouter, Query
from pydantic import BaseModel

from chatbot.dialogue_manager import detect_lang_auto
from chatbot.retriever_neo4j import Neo4jRetriever
from chatbot.db import SessionLocal, ChatMessage   # ✅ thêm để lưu DB

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])

SESSIONS: Dict[str, Dict] = {}

retriever = Neo4jRetriever(
    uri=os.getenv("NEO4J_URI", "bolt://localhost:7687"),
    user=os.getenv("NEO4J_USER", "neo4j"),
    password=os.getenv("NEO4J_PASS", "BENCHAN2025"),
)

class ChatIn(BaseModel):
    session_id: str
    text: str

# ---------- helper save DB ----------
def save_message(session_id, role, lang, text, meta=None):
    db = SessionLocal()
    try:
        msg = ChatMessage(
            session_id=session_id,
            role=role,
            lang=lang,
            text=text,
            meta=meta
        )
        db.add(msg)
        db.commit()
    finally:
        db.close()

# ---------- helpers ----------
def topic_from_question(q: str) -> str:
    s = (q or "").lower()
    if any(k in s for k in ["nhãn hiệu", "thuong hieu", "trademark", "brand"]):
        return "trademark"
    if any(k in s for k in ["bản quyền", "ban quyen", "quyền tác giả", "copyright"]):
        return "copyright"
    if any(k in s for k in ["sáng chế", "sang che", "patent"]):
        return "patent"
    if any(k in s for k in ["kiểu dáng", "kieu dang", "industrial design", "design"]):
        return "design"
    return "ip"

def extract_focus_terms(q: str) -> Tuple[List[str], List[str]]:
    s = (q or "").lower()
    must, prefer = [], []

    def add(*xs):
        for x in xs:
            if x and x not in must:
                must.append(x)

    if any(k in s for k in ["điện ảnh", "dien anh", "phim", "cinema", "cinematograph"]):
        add("điện ảnh", "phim", "cinematograph")
    if any(k in s for k in ["chương trình máy tính", "chuong trinh may tinh", "computer program", "software"]):
        add("chương trình máy tính", "program", "phần mềm")
    if any(k in s for k in ["kiến trúc", "kien truc", "architecture"]):
        add("kiến trúc", "architecture")
    if any(k in s for k in ["bài giảng", "bai giang", "bài phát biểu", "bai phat bieu", "bài nói", "bai noi", "lecture", "speech"]):
        add("bài giảng", "bài phát biểu")
    if any(k in s for k in ["biểu diễn", "bieu dien", "performance"]):
        add("biểu diễn", "performance")
    if any(k in s for k in ["ghi âm", "ghi hinh", "ban ghi am", "ban ghi hinh", "phonogram", "video recording"]):
        add("ghi âm", "ghi hình")
    if any(k in s for k in ["phát sóng", "phat song", "broadcast"]):
        add("phát sóng", "broadcast")

    if any(k in s for k in ["nổi tiếng", "noi tieng", "well-known"]):
        add("nhãn hiệu nổi tiếng")

    if any(k in s for k in ["đăng ký", "dang ky", "register", "registration"]):
        prefer += ["đăng ký", "hồ sơ", "thẩm quyền", "giấy chứng nhận"]
    if any(k in s for k in ["xâm phạm", "sao chép", "chiem dung", "vi pham", "infringe", "copy"]):
        prefer += ["hành vi xâm phạm", "xử phạt", "biện pháp dân sự", "bồi thường"]

    must   = [t for i,t in enumerate(must)   if len(t)>=2 and t not in must[:i]]
    prefer = [t for i,t in enumerate(prefer) if len(t)>=2 and t not in prefer[:i]]
    return must, prefer

def build_reply(lang: str, topic: str) -> str:
    if lang == "JP":
        base = "以下に関連する法令条文を提示しました。必要であれば弁護士の連絡先も載せています。"
        tip = {
            "copyright": "著作権の登録・保護に関する条文です。",
            "trademark": "商標の登録・保護に関する条文です。",
            "patent": "特許の出願・保護に関する条文です。",
            "design": "意匠の出願・保護に関する条文です。",
            "ip": "知的財産全般に関する条文です。",
        }.get(topic, "知的財産全般に関する条文です。")
        return f"{tip} {base}"
    if lang == "EN":
        base = "I’ve pulled relevant legal provisions below. Lawyer suggestions are included."
        tip = {
            "copyright": "Here are provisions about copyright registration and protection.",
            "trademark": "Here are provisions about trademark registration and protection.",
            "patent": "Here are provisions about patent filing and protection.",
            "design": "Here are provisions about industrial design filing and protection.",
            "ip": "Here are provisions related to intellectual property.",
        }.get(topic, "Here are provisions related to intellectual property.")
        return f"{tip} {base}"
    base = "Mình đã gợi ý các điều luật liên quan bên dưới (kèm luật sư hỗ trợ)."
    tip = {
        "copyright": "Các điều khoản về đăng ký & bảo hộ quyền tác giả.",
        "trademark": "Các điều khoản về đăng ký & bảo hộ nhãn hiệu.",
        "patent": "Các điều khoản về nộp đơn & bảo hộ sáng chế.",
        "design": "Các điều khoản về nộp đơn & bảo hộ kiểu dáng.",
        "ip": "Các điều khoản liên quan tới sở hữu trí tuệ.",
    }.get(topic, "Các điều khoản liên quan tới sở hữu trí tuệ.")
    return f"{tip} {base}"

# ---------- endpoint ----------
@router.post("/chat")
def chat(payload: ChatIn):
    text = payload.text or ""
    lang = detect_lang_auto(text)
    topic = topic_from_question(text)
    must_terms, prefer_terms = extract_focus_terms(text)

    # ✅ lưu tin nhắn user
    save_message(session_id=payload.session_id, role="user", lang=lang, text=text)

    articles: List[Dict] = []
    lawyers: List[Dict] = []
    links: List[str] = []

    if retriever and retriever.ready:
        # 1) Ưu tiên match theo tiêu đề
        law_arts, dec_arts = retriever.search_articles_and_decrees_by_title(
            question=text,
            lang=lang,
            limit_total=12,
            must_terms=must_terms,
            prefer_terms=prefer_terms
        )
        articles = [*law_arts, *dec_arts]

        # 2) Fallback: quét nội dung khoản
        if not articles:
            articles = retriever.search_clauses(
                question=text,
                topic=topic or "",
                lang=lang,
                limit=12,
                prefer_terms=prefer_terms
            )

        # 3) Gợi ý luật sư
        lawyers = retriever.search_lawyers(topic=topic or "IP Law", lang=lang, limit=3)

        # 4) Links nguồn
        for a in articles:
            lk = (a.get("law") or {}).get("link")
            if lk:
                links.append(lk)
        links = list(dict.fromkeys(links))

    reply = build_reply(lang, topic)
    state = {"topic": topic, "registered": None}
    SESSIONS[payload.session_id] = state

    # ✅ lưu tin nhắn bot
    save_message(session_id=payload.session_id, role="assistant", lang=lang, text=reply)

    print(f"[DBG] lang={lang} topic={topic} must={must_terms} prefer={prefer_terms} arts={len(articles)} lw={len(lawyers)}")

    return {
        "reply": reply,
        "ARTICLES": articles,
        "LAWYERS": lawyers,
        "links": links,
        "state": state,
        "lang": lang,
    }

# ---------- API get history ----------
@router.get("/history")
def get_history(session_id: str = Query(...)):
    db = SessionLocal()
    try:
        msgs = (
            db.query(ChatMessage)
            .filter(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.ts)
            .all()
        )
        return [
            {
                "role": m.role,
                "lang": m.lang,
                "text": m.text,
                "ts": m.ts.isoformat()
            }
            for m in msgs
        ]
    finally:
        db.close()

# ---------- API get all sessions ----------
@router.get("/sessions")
def get_sessions():
    db = SessionLocal()
    try:
        rows = db.query(ChatMessage.session_id).distinct().all()
        return [r[0] for r in rows]
    finally:
        db.close()
