# app/qa_ip.py
from fastapi import APIRouter
from pydantic import BaseModel
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer, util

router = APIRouter()

# Neo4j connection
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "BENCHAN2025"))

# Load multilingual model
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

# Request body
class AskRequest(BaseModel):
    question: str
    top_k: int = 3

@router.post("/ask-ip")
def ask_ip(req: AskRequest):
    q_emb = model.encode(req.question, convert_to_tensor=True)

    with driver.session() as session:
        cypher = """
        MATCH (a:Article)-[:HAS_CLAUSE]->(c:Clause)
        RETURN a.ARTICLE_ID AS articleId,
               a.NUMBER AS articleNumber,
               a.TITLE_EN AS articleTitle,
               collect({
                   id: c.CLAUSE_ID,
                   number: c.NUMBER,
                   text_en: c.TEXT_EN,
                   text_vn: c.TEXT_VN,
                   text_jp: c.TEXT_JP
               }) AS clauses
        """
        records = session.run(cypher).data()

    articles = []
    for r in records:
        scored_clauses = []
        for c in r["clauses"]:
            text = c.get("text_en") or c.get("text_vn") or c.get("text_jp") or ""
            if not text:
                continue
            c_emb = model.encode(text, convert_to_tensor=True)
            score = float(util.cos_sim(q_emb, c_emb))
            c["score"] = score
            scored_clauses.append(c)

        scored_clauses = sorted(scored_clauses, key=lambda x: x["score"], reverse=True)[:req.top_k]

        if scored_clauses:
            articles.append({
                "id": r["articleId"],
                "number": r["articleNumber"],
                "title": r["articleTitle"],
                "clauses": scored_clauses
            })

    # Query lawyers demo
    lawyer_cypher = """
    MATCH (l:Lawyer)
    WHERE l.SPECIALTY_EN CONTAINS 'Intellectual Property'
    RETURN l.LAWYER_ID AS id, 
           l.NAME_EN AS name_en, l.NAME_VN AS name_vn, l.NAME_JP AS name_jp,
           l.FIRM_EN AS firm_en, l.FIRM_VN AS firm_vn, l.FIRM_JP AS firm_jp,
           l.SPECIALTY_EN AS specialty_en,
           l.EMAIL AS email,
           l.TELEPHONE_NUMBER AS phone
    LIMIT 2
    """
    with driver.session() as session:
        lawyer_records = session.run(lawyer_cypher).data()

    lawyers = []
    for l in lawyer_records:
        lawyers.append({
            "id": l["id"],
            "name_en": l["name_en"], "name_vn": l["name_vn"], "name_jp": l["name_jp"],
            "firm_en": l["firm_en"], "firm_vn": l["firm_vn"], "firm_jp": l["firm_jp"],
            "specialty_en": l["specialty_en"],
            "email": l["email"], "phone": l["phone"]
        })

    return {
        "ARTICLES": articles,
        "LAWYERS": lawyers
    }
