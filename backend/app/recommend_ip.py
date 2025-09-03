from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer, util
import os
from dotenv import load_dotenv

# ====== Load env ======
load_dotenv()
URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USER = os.getenv("NEO4J_USER", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

# ====== Load model embeddings ======
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# ====== Kết nối Neo4j ======
driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))


# ====== Tìm điều khoản phù hợp ======
def recommend_clauses(question: str, top_k: int = 3):
    keywords_en = ["register", "registration", "application", "procedure",
                   "trademark", "copyright", "patent", "design"]
    keywords_vn = ["đăng ký", "thủ tục", "đơn", "nhãn hiệu",
                   "bản quyền", "sáng chế", "kiểu dáng"]
    keywords_jp = ["登録", "手続", "申請", "商標", "著作権", "特許", "意匠"]

    keywords = keywords_en + keywords_vn + keywords_jp

    where_clause = " OR ".join(
        [f"toLower(c.TEXT_EN) CONTAINS '{kw.lower()}'" for kw in keywords] +
        [f"toLower(c.TEXT_VN) CONTAINS '{kw.lower()}'" for kw in keywords] +
        [f"toLower(c.TEXT_JP) CONTAINS '{kw}'" for kw in keywords_jp]
    )

    with driver.session() as session:
        query = f"""
        MATCH (c:Clause)
        WHERE {where_clause}
        RETURN c.CLAUSE_ID as id, 
               c.TEXT_EN as text_en, 
               c.TEXT_VN as text_vn, 
               c.TEXT_JP as text_jp,
               c.NUMBER as number,
               c.ARTICLE_ID as article_id
        """
        results = session.run(query)
        clauses = [dict(r) for r in results]

    if not clauses:
        with driver.session() as session:
            query = """
            MATCH (c:Clause)
            RETURN c.CLAUSE_ID as id, 
                   c.TEXT_EN as text_en, 
                   c.TEXT_VN as text_vn, 
                   c.TEXT_JP as text_jp,
                   c.NUMBER as number,
                   c.ARTICLE_ID as article_id
            """
            results = session.run(query)
            clauses = [dict(r) for r in results]

    if not clauses:
        return []

    q_emb = model.encode(question, convert_to_tensor=True)
    texts = [c["text_en"] or c["text_vn"] or c["text_jp"] or "" for c in clauses]
    c_embs = model.encode(texts, convert_to_tensor=True)

    scores = util.cos_sim(q_emb, c_embs)[0].cpu().numpy()

    for i, c in enumerate(clauses):
        c["score"] = float(scores[i])

    clauses = sorted(clauses, key=lambda x: x["score"], reverse=True)
    return clauses[:top_k]


# ====== Recommend Lawyers ======
def recommend_lawyers(question: str, top_k: int = 2):
    if "trademark" not in question.lower():
        return []

    with driver.session() as session:
        query = """
        MATCH (l:Lawyer)
        WHERE l.SPECIALTY_EN CONTAINS 'Intellectual Property'
        RETURN l.LAWYER_ID as id, 
               l.NAME_EN as name_en, l.NAME_VN as name_vn, l.NAME_JP as name_jp,
               l.FIRM_EN as firm_en, l.FIRM_VN as firm_vn, l.FIRM_JP as firm_jp,
               l.SPECIALTY_EN as specialty_en,
               l.EMAIL as email,
               l.TELEPHONE_NUMBER as phone
        LIMIT $top_k
        """
        results = session.run(query, top_k=top_k)
        lawyers = [dict(r) for r in results]

    return lawyers


# ====== Hàm tổng hợp gọi từ API ======
def get_recommendations(question: str, top_k: int = 3):
    clauses = recommend_clauses(question, top_k=top_k)
    lawyers = recommend_lawyers(question, top_k=2)
    return {"CLAUSES": clauses, "LAWYERS": lawyers}


if __name__ == "__main__":
    q = "How to register trademark in Vietnam?"
    res = get_recommendations(q, top_k=3)
    print(res)
