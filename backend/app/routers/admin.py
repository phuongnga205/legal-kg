from fastapi import APIRouter, HTTPException
from app.db import driver

# 👇 thêm prefix="/api/admin" để không bị lặp đường dẫn
router = APIRouter(prefix="/api/admin", tags=["Admin"])

@router.get("/stats")
async def get_stats():
    with driver.session() as session:
        total = session.run("MATCH (c:Case) RETURN count(c) AS total").single()["total"]
        analyzed = session.run("MATCH (c:Case {status:'Analyzed'}) RETURN count(c) AS analyzed").single()["analyzed"]
        spam = session.run("MATCH (c:Case {quality:'Spam'}) RETURN count(c) AS spam").single()["spam"]
        pending = session.run("MATCH (c:Case {status:'Pending'}) RETURN count(c) AS pending").single()["pending"]

        return {
            "total": total,
            "analyzed": analyzed,
            "spam": spam,
            "pending": pending
        }

@router.get("/conversations")
async def get_conversations():
    with driver.session() as session:
        result = session.run("""
            MATCH (c:Case)<-[:ASKED]-(u:User)
            RETURN c.case_id as id,
                   u.name as customer,
                   u.phone as phone,
                   c.quality as quality,
                   c.status as status,
                   c.createdAt as createdAt
            ORDER BY c.createdAt DESC
            LIMIT 50
        """)
        return [dict(r) for r in result]

@router.get("/conversation/{case_id}")
async def get_conversation(case_id: str):
    with driver.session() as session:
        result = session.run("""
            MATCH (c:Case {case_id:$case_id})<-[:ASKED]-(u:User)
            OPTIONAL MATCH (c)-[:HAS_MESSAGE]->(m:Message)
            RETURN u.name as customer, u.phone as phone,
                   c.case_id as id, c.status as status,
                   collect({role:m.role, text:m.text, time:m.createdAt}) as messages
        """, case_id=case_id).single()
        if not result:
            raise HTTPException(404, "Conversation not found")
        return dict(result)
