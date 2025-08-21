from neo4j import GraphDatabase
import os, time, uuid
from .config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def upsert_user_and_create_case(user: dict, question: str, lang: str):
    user_id = user.get("id") or str(uuid.uuid4())
    case_id = str(uuid.uuid4())
    now = int(time.time() * 1000)

    cypher = """
    MERGE (u:User {user_id: $user_id})
      ON CREATE SET u.email = $email, u.name = $name, u.createdAt = $now
      ON MATCH  SET u.email = coalesce($email, u.email), 
                  u.name = coalesce($name, u.name), 
                  u.updatedAt = $now
    CREATE (c:Case {case_id: $case_id, question: $question, lang: $lang, createdAt: $now})
    MERGE (u)-[:ASKED {createdAt: $now}]->(c)
    RETURN u.user_id AS user_id, c.case_id AS case_id
    """
    with driver.session() as session:
        rec = session.run(cypher, {
            "user_id": user_id,
            "email": user.get("email"),
            "name": user.get("name"),
            "case_id": case_id,
            "question": question,
            "lang": lang,
            "now": now
        }).single()
        return {"USER_ID": rec["user_id"], "CASE_ID": rec["case_id"]}
