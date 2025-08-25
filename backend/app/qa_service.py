from ..db import driver

def find_clauses(question: str, lang: str):
    field = {
        "vi": "TEXT_VN",
        "en": "TEXT_EN",
        "jp": "TEXT_JP"
    }.get(lang.lower(), "TEXT_EN")

    title_field = {
        "vi": "TITLE_VN",
        "en": "TITLE_EN",
        "jp": "TITLE_JP"
    }.get(lang.lower(), "TITLE_EN")

    with driver.session() as session:
        cypher = f"""
        MATCH (c:Clause)<-[:HAS_CLAUSE]-(a:Article)
        OPTIONAL MATCH (a)<-[:LAW_HAS_ARTICLE]-(l:Law)
        OPTIONAL MATCH (a)<-[:DECREE_HAS_ARTICLE]-(d:Decree)
        WHERE toLower(c.{field}) CONTAINS toLower($q)
           OR toLower(a.{title_field}) CONTAINS toLower($q)
           OR toLower(l.NAME_EN) CONTAINS toLower($q)
           OR toLower(d.NAME_EN) CONTAINS toLower($q)
        RETURN c.CLAUSE_ID as CLAUSE_ID,
               c.NUMBER as CLAUSE_NUMBER,
               c.{field} as CLAUSE_TEXT,
               a.ARTICLE_ID as ARTICLE_ID,
               a.NUMBER as ARTICLE_NUMBER,
               a.{title_field} as ARTICLE_TITLE,
               l.LAW_ID as LAW_ID,
               l.NAME_EN as LAW_NAME,
               d.DECREE_ID as DECREE_ID,
               d.NAME_EN as DECREE_NAME
        LIMIT 5
        """
        result = session.run(cypher, q=question)
        clauses = [dict(r) for r in result]

    summary = f"Found {len(clauses)} clauses/articles related to '{question}'"
    return {
        "summary": summary,
        "clauses": [
            {
                "TITLE": f"Clause {c['CLAUSE_NUMBER']} (Article {c['ARTICLE_NUMBER']})",
                "TEXT": c["CLAUSE_TEXT"]
            }
            for c in clauses
        ]
    }
