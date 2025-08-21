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

ARTICLE_RE = re.compile(r"\barticle\s*(\d+)\b", re.I)
CLAUSE_RE = re.compile(r"\bclause\s*(\d+)\b", re.I)
DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")

INTENT_PATTERNS = [
    (re.compile(r"\b(article|clause)\b", re.I), "GET_ARTICLE_OR_CLAUSE"),
    (re.compile(r"\b(law|decree|ip law|intellectual property)\b", re.I), "SEARCH_NORM"),
    (re.compile(r"\beffective\b|\bvalid from\b|\bexpire|expired|expiry\b", re.I), "FILTER_BY_DATE"),
]

def parse_intent(text: str) -> ParsedQuery:
    doc = nlp(text)

    intent = "SEARCH_NORM"
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
        keywords = " ".join(chunks[:6]) if chunks else None

    return ParsedQuery(intent=intent, article_no=art, clause_no=cl,
                       keywords=keywords, date_from=date_from, date_to=date_to)

# --------- Cypher builders (match schema) ----------

def cypher_get_article_clause(p: ParsedQuery) -> Tuple[str, Dict[str, Any]]:
    """
    Truy vấn theo Article / Clause từ cả Law và Decree (do Article có thể thuộc Law hoặc Decree).
    Dùng quan hệ: (Law)-[:LAW_HAS_ARTICLE]->(Article), (Decree)-[:DECREE_HAS_ARTICLE]->(Article)
                  (Article)-[:HAS_CLAUSE]->(Clause)
    Thuộc tính dùng NAME_VN/EN/JP; TITLE_VN/EN/JP; TEXT_VN/EN/JP;
    Hỗ trợ cả INTRODUCTORY_STATEMENT_* hoặc 'INTRODUCTORY STATEMENT_*' (có dấu cách).
    """
    # Chỉ Article
    if p.article_no is not None and p.clause_no is None:
        q = """
        // Article từ Law
        MATCH (l:Law)-[:LAW_HAS_ARTICLE]->(a:Article {NUMBER: $article_no})
        OPTIONAL MATCH (a)-[:HAS_CLAUSE]->(c1:Clause)
        WITH l, a, collect({clause: c1.NUMBER, text_vn: c1.TEXT_VN, text_en: c1.TEXT_EN, text_jp: c1.TEXT_JP}) AS clausesL

        // Article từ Decree (cùng NUMBER)
        OPTIONAL MATCH (d:Decree)-[:DECREE_HAS_ARTICLE]->(a2:Article {NUMBER: $article_no})
        OPTIONAL MATCH (a2)-[:HAS_CLAUSE]->(c2:Clause)
        WITH l, a, clausesL, d, a2, collect({clause: c2.NUMBER, text_vn: c2.TEXT_VN, text_en: c2.TEXT_EN, text_jp: c2.TEXT_JP}) AS clausesD

        RETURN
          coalesce(l.LAW_ID, '') AS law_id,
          coalesce(l.NAME_EN, l.NAME_VN, l.NAME_JP, '') AS law_name,
          coalesce(d.DECREE_ID, '') AS decree_id,
          coalesce(d.NAME_EN, d.NAME_VN, d.NAME_JP, '') AS decree_name,
          coalesce(a.NUMBER, a2.NUMBER) AS article_number,
          coalesce(a.TITLE_EN, a.TITLE_VN, a.TITLE_JP, a2.TITLE_EN, a2.TITLE_VN, a2.TITLE_JP) AS article_title,
          coalesce(a.INTRODUCTORY_STATEMENT_EN, a.`INTRODUCTORY STATEMENT_EN`,
                   a.INTRODUCTORY_STATEMENT_VN, a.`INTRODUCTORY STATEMENT_VN`,
                   a.INTRODUCTORY_STATEMENT_JP, a.`INTRODUCTORY STATEMENT_JP`) AS intro_statement_a,
          coalesce(a2.INTRODUCTORY_STATEMENT_EN, a2.`INTRODUCTORY STATEMENT_EN`,
                   a2.INTRODUCTORY_STATEMENT_VN, a2.`INTRODUCTORY STATEMENT_VN`,
                   a2.INTRODUCTORY_STATEMENT_JP, a2.`INTRODUCTORY STATEMENT_JP`) AS intro_statement_a2,
          CASE WHEN a IS NOT NULL THEN clausesL ELSE clausesD END AS clauses
        ORDER BY article_number
        """
        return q, {"article_no": p.article_no}

    # Article + Clause
    if p.article_no is not None and p.clause_no is not None:
        q = """
        // Clause thuộc Article thuộc Law
        OPTIONAL MATCH (l:Law)-[:LAW_HAS_ARTICLE]->(a:Article {NUMBER: $article_no})
        OPTIONAL MATCH (a)-[:HAS_CLAUSE]->(c:Clause {NUMBER: $clause_no})

        // Clause thuộc Article thuộc Decree
        OPTIONAL MATCH (d:Decree)-[:DECREE_HAS_ARTICLE]->(a2:Article {NUMBER: $article_no})
        OPTIONAL MATCH (a2)-[:HAS_CLAUSE]->(c2:Clause {NUMBER: $clause_no})

        WITH l, d, a, a2, c, c2
        RETURN
          coalesce(l.LAW_ID, '') AS law_id,
          coalesce(l.NAME_EN, l.NAME_VN, l.NAME_JP, '') AS law_name,
          coalesce(d.DECREE_ID, '') AS decree_id,
          coalesce(d.NAME_EN, d.NAME_VN, d.NAME_JP, '') AS decree_name,
          coalesce(a.NUMBER, a2.NUMBER) AS article_number,
          coalesce(c.NUMBER, c2.NUMBER) AS clause_number,
          coalesce(c.TEXT_EN, c2.TEXT_EN, c.TEXT_VN, c2.TEXT_VN, c.TEXT_JP, c2.TEXT_JP) AS text_main,
          c.TEXT_VN AS text_vn_law,  c.TEXT_EN AS text_en_law,  c.TEXT_JP AS text_jp_law,
          c2.TEXT_VN AS text_vn_dec, c2.TEXT_EN AS text_en_dec, c2.TEXT_JP AS text_jp_dec
        """
        return q, {"article_no": p.article_no, "clause_no": p.clause_no}

    # fallback
    return cypher_search_norm(p)

def cypher_search_norm(p: ParsedQuery) -> Tuple[str, Dict[str, Any]]:
    """
    Tìm theo từ khóa trong Law/Decree/Article/Clause (VN/EN/JP), lọc theo EFFECTIVE_DATE/EXPIRY_DATE của Law/Decree.
    Chấp nhận EFFECTIVE_DATE/EXPIRY_DATE là string ISO -> ép date().
    """
    q = """
    // Gom ứng viên theo từ khóa
    CALL {
      WITH $kw AS kw
      MATCH (l:Law)
      OPTIONAL MATCH (l)-[:LAW_HAS_ARTICLE]->(a:Article)
      OPTIONAL MATCH (a)-[:HAS_CLAUSE]->(c:Clause)
      WHERE kw IS NULL OR
            toLower(coalesce(l.NAME_EN,'')) CONTAINS toLower(kw) OR
            toLower(coalesce(l.NAME_VN,'')) CONTAINS toLower(kw) OR
            toLower(coalesce(l.NAME_JP,'')) CONTAINS toLower(kw) OR
            toLower(coalesce(a.TITLE_EN,'')) CONTAINS toLower(kw) OR
            toLower(coalesce(a.TITLE_VN,'')) CONTAINS toLower(kw) OR
            toLower(coalesce(a.TITLE_JP,'')) CONTAINS toLower(kw) OR
            toLower(coalesce(c.TEXT_EN,''))  CONTAINS toLower(kw) OR
            toLower(coalesce(c.TEXT_VN,''))  CONTAINS toLower(kw) OR
            toLower(coalesce(c.TEXT_JP,''))  CONTAINS toLower(kw)
      RETURN l, a, c
    }
    WITH DISTINCT l, a, c
    WHERE
      ($date_from IS NULL OR date(coalesce(l.EFFECTIVE_DATE, '0001-01-01')) >= date($date_from)) AND
      ($date_to   IS NULL OR date(coalesce(l.EXPIRY_DATE,   '9999-12-31')) <= date($date_to))
    WITH l, collect(DISTINCT a) AS arts, collect(DISTINCT c) AS clauses
    RETURN l.LAW_ID AS law_id,
           coalesce(l.NAME_EN, l.NAME_VN, l.NAME_JP, '') AS law_name,
           collect(x IN arts | x.NUMBER) AS article_numbers,
           size([x IN clauses WHERE x IS NOT NULL]) AS clauses_count,
           l.EFFECTIVE_DATE AS effective_date,
           l.EXPIRY_DATE AS expiry_date,
           coalesce(l.STATUS_EN, l.STATUS_VN, l.STATUS_JP, '') AS status,
           l.LINK AS link
    ORDER BY clauses_count DESC, law_name ASC
    LIMIT 50
    """
    params = {"kw": p.keywords, "date_from": p.date_from, "date_to": p.date_to}
    return q, params

def build_cypher(user_text: str) -> Tuple[str, Dict[str, Any]]:
    p = parse_intent(user_text)
    if p.intent == "GET_ARTICLE_OR_CLAUSE":
        return cypher_get_article_clause(p)
    else:
        return cypher_search_norm(p)

def run_cypher(query: str, params: Dict[str, Any]) -> list:
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    with driver.session() as session:
        res = session.run(query, **params)
        return [r.data() for r in res]

def main():
    ap = argparse.ArgumentParser(description="IP QA: Natural language → Cypher (aligned with LAW/DECREE schema)")
    ap.add_argument("question", type=str, help="User question (EN/VN/JP)")
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
