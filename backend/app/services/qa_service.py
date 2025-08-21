from app.services.qa_ip import build_cypher, run_cypher

def find_clauses(question: str, lang: str):
    q, params = build_cypher(question)
    rows = run_cypher(q, params)

    clauses = []
    for r in rows:
        # normalize dữ liệu
        clause_text = r.get("text_main") or r.get("intro_statement_a") or r.get("intro_statement_a2")
        clauses.append({
            "TITLE": r.get("article_title") or r.get("law_name") or r.get("decree_name") or "Untitled",
            "TEXT": clause_text or "",
        })

    return {
        "summary": f"Found {len(clauses)} clause(s) for: {question}",
        "clauses": clauses
    }
