from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from ..db import upsert_user_and_create_case
from ..services.qa_service import find_clauses
from ..services.reco_service import recommend_lawyers

router = APIRouter()

class UserIn(BaseModel):
    id: Optional[str] = None
    email: Optional[EmailStr] = None
    name: Optional[str] = None

class AskIPRequest(BaseModel):
    question: str
    lang: str = "vi"
    user: UserIn

class ClauseOut(BaseModel):
    TITLE: str
    TEXT: str

class LawyerOut(BaseModel):
    NAME: str
    FIRM: Optional[str] = None
    SPECIALTY: Optional[str] = None
    CONTACT: Optional[str] = None
    SCORE: Optional[float] = None

class AskIPResponse(BaseModel):
    CASE_ID: str
    USER_ID: str
    SUMMARY: str
    CLAUSES: List[ClauseOut]
    LAWYERS: List[LawyerOut]

@router.post("/ask-ip", response_model=AskIPResponse)
def ask_ip(req: AskIPRequest):
    print(">>> [ask_ip] Request:", req.dict())   # 🚀 log request
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        ids = upsert_user_and_create_case(req.user.dict(), req.question, req.lang)
        print(">>> [ask_ip] ids:", ids)

        qa = find_clauses(req.question, req.lang)
        print(">>> [ask_ip] qa:", qa)

        recos = recommend_lawyers(req.question, req.lang)
        print(">>> [ask_ip] recos:", recos)

        return AskIPResponse(
            CASE_ID=ids["CASE_ID"],
            USER_ID=ids["USER_ID"],
            SUMMARY=qa["summary"],
            CLAUSES=qa["clauses"],
            LAWYERS=recos,
        )
    except Exception as e:
        print(">>> [ask_ip] ERROR:", e)  # 🚀 in lỗi ra console
        raise
