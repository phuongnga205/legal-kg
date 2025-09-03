# app/routers/lawyer.py
from fastapi import APIRouter
from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

router = APIRouter()

# Load .env
load_dotenv()
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASS = os.getenv("NEO4J_PASS", "BENCHAN2025")

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))

@router.get("/lawyers")
def get_lawyers():
    cypher = """
    MATCH (l:Lawyer)
    RETURN l.LAWYER_ID as id,
           l.NAME_VN as name_vn,
           l.NAME_EN as name_en,
           l.NAME_JP as name_jp,
           l.SPECIALTY_VN as specialty_vn,
           l.SPECIALTY_EN as specialty_en,
           l.SPECIALTY_JP as specialty_jp,
           l.FIRM_VN as firm_vn,
           l.FIRM_EN as firm_en,
           l.FIRM_JP as firm_jp,
           l.TELEPHONE_NUMBER as phone,
           l.EMAIL as email
    ORDER BY name_vn
    """
    with driver.session() as session:
        result = session.run(cypher)
        lawyers = [dict(record) for record in result]
    return {"lawyers": lawyers}
