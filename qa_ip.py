# qa_ip.py
import os
import re
import json
import argparse
from dataclasses import dataclass
from typing import Dict, Any, Optional, Tuple

import spacy
from dotenv import load_dotenv
from neo4j import GraphDatabase

# ---------- Config ----------
load_dotenv()
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "neo4j")

# Load spaCy English model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    raise SystemExit("spaCy model not found. Run: python -m spacy download en_core_web_sm")

@dataclass
class ParsedQuery:
    intent: str
    article_no: Optional[int] = None
    clause_no: Optional[int] = None
    keywords: Optional[str] = None
    date_from: Optional[str] = None  # YYYY-MM-DD
    date_to: Optional[str] = None    # YYYY-MM-DD

ARTICLE_RE = re.compile(r"article\s*(\d+)", re.I)
CLAUSE_RE = re.compile(r"clause\s*(\d+)", re.I)
DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")

INTENT_PATTERNS = [
    (re.compile(r"\b(article|clause)\b", re.I), "GET_ARTICLE_OR_CLAUSE"),
    (re.compile(r"\b(law|ip law|intellectual property)\b", re.I), "SEARCH_LAW"),
    (re.compile(r"\beffective\b|\bvalid from\b|\bexpire\b", re.I), "FILTER_BY_DATE"),
]

def parse_intent(text: str) -> ParsedQuery:
    doc = nlp(text)

    intent = "SEARCH_LAW"
    for pat, name in INTENT_PATTERNS:
        if pat.search(text):
            intent = name
            break

    art = None
    cl = None
    if m := ARTICLE_RE.search(text):
        art = int(m.group(1))
    if m := CLAUSE_RE.search(text):
        cl = int(m.group(1))

    dates = DATE_RE.findall(text)
    date_from = dates[0] if len(dates) >= 1 else None
    date_to = dates[1] if len(dates) >= 2 else None

    quoted = re.findall(r'"([^"]+)"', text)
    if quoted:
        keywords = " ".join(quoted)
    else:
        chunks = [c.text for c in doc.noun_chunks]
        keywords = " ".join(chunks[:4]) if chunks else None

    return ParsedQuery(intent=intent, article_no=art, clause_no=cl,
                       keywords=keywords, date_from=date_from, date_to=date_to)

def cypher_get_article_clause(p: ParsedQuery) -> Tuple[str, Dict[str, Any]]:
    if p.article_no is None:
        return cypher_search_law(p)

    if p.clause_no is None:
        q = (
            """
            MATCH (a:Article {NUMBER: $article_no})<-[:HAS_ARTICLE]-(l:Law)
            OPTIONAL MATCH (a)-[:HAS_CLAUSE]->(c:Clause)
            RETURN l.LAW_ID AS law_id, l.NAME_EN AS law_en, a.NUMBER AS article, a.TITLE_EN AS article_title,
                   collect({clause: c.NUMBER, text_en: c.TEXT_EN, text_vn: c.TEXT_VN, text_jp: c.TEXT_JP}) AS clauses
            ORDER BY article
            """
        )
        params = {"article_no": p.article_no}
        return q, params
    else:
        q = (
            """
            MATCH (a:Article {NUMBER: $article_no})<-[:HAS_ARTICLE]-(l:Law)
            MATCH (a)-[:HAS_CLAUSE]->(c:Clause {NUMBER: $clause_no})
            RETURN l.LAW_ID AS law_id, l.NAME_EN AS law_en, a.NUMBER AS article,
                   c.NUMBER AS clause, c.TEXT_EN AS text_en, c.TEXT_VN AS text_vn, c.TEXT_JP AS text_jp
            """
        )
        params = {"article_no": p.article_no, "clause_no": p.clause_no}
        return q, params

def cypher_search_law(p: ParsedQuery) -> Tuple[str, Dict[str, Any]]:
    q = (
        """
        CALL {
          WITH $kw AS kw
          MATCH (l:Law)
          OPTIONAL MATCH (l)-[:HAS_ARTICLE]->(a:Article)
          OPTIONAL MATCH (a)-[:HAS_CLAUSE]->(c:Clause)
          WHERE kw IS NULL OR toLower(l.NAME_EN) CONTAINS toLower(kw)
             OR toLower(a.TITLE_EN) CONTAINS toLower(kw)
             OR toLower(c.TEXT_EN) CONTAINS toLower(kw)
          RETURN l, a, c
        }
        WITH DISTINCT l, a, c
        WHERE ($date_from IS NULL OR l.EFFECTIVE_DATE >= date($date_from))
          AND ($date_to   IS NULL OR coalesce(l.EXPIRY_DATE, date('9999-12-31')) <= date($date_to))
        RETURN l.LAW_ID AS law_id, l.NAME_EN AS law_en,
               collect(DISTINCT a.NUMBER) AS articles,
               size([x IN collect(DISTINCT c) WHERE x IS NOT NULL]) AS clauses_count
        ORDER BY clauses_count DESC
        LIMIT 30
        """
    )
    params = {"kw": p.keywords, "date_from": p.date_from, "date_to": p.date_to}
    return q, params

def build_cypher(user_text: str) -> Tuple[str, Dict[str, Any]]:
    p = parse_intent(user_text)
    if p.intent == "GET_ARTICLE_OR_CLAUSE":
        return cypher_get_article_clause(p)
    else:
        return cypher_search_law(p)

def run_cypher(query: str, params: Dict[str, Any]) -> list:
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    with driver.session() as session:
        res = session.run(query, **params)
        return [r.data() for r in res]

def main():
    ap = argparse.ArgumentParser(description="IP QA: Natural language → Cypher")
    ap.add_argument("question", type=str, help="User question in English")
    ap.add_argument("--dry-run", action="store_true", help="Only print Cypher")
    ap.add_argument("--run", action="store_true", help="Execute query against Neo4j")
    args = ap.parse_args()

    q, params = build_cypher(args.question)
    print("\n[Cypher]\n", q)
    print("\n[Params]", json.dumps(params, ensure_ascii=False))

    if args.run:
        rows = run_cypher(q, params)
        print("\n[Rows]", json.dumps(rows, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
