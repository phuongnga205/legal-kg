# -*- coding: utf-8 -*-
from typing import List, Dict, Tuple, Any
from neo4j import GraphDatabase
import os
from googletrans import Translator

translator = Translator()

LAW_LABELS     = ["LAW", "Law"]
DECREE_LABELS  = ["DECREE", "Decree"]
ARTICLE_LABELS = ["ARTICLE", "Article"]
CLAUSE_LABELS  = ["CLAUSE", "Clause"]
LAWYER_LABELS  = ["LAWYER", "Lawyer"]


def _pick_title(r: Dict, lang: str) -> str:
    if lang == "VN":
        return r.get("article_title_vn") or r.get("law_name_vn") or r.get("decree_name_vn") or ""
    if lang == "JP":
        return r.get("article_title_jp") or r.get("law_name_jp") or r.get("decree_name_jp") or ""
    return r.get("article_title_en") or r.get("law_name_en") or r.get("decree_name_en") or ""


def _resolve_clause_text(cl: Dict, lang: str) -> str:
    if lang == "VN":
        return cl.get("text_vn") or cl.get("text_en") or cl.get("text_jp") or ""
    if lang == "JP":
        return cl.get("text_jp") or cl.get("text_en") or cl.get("text_vn") or ""
    return cl.get("text_en") or cl.get("text_vn") or cl.get("text_jp") or ""


class Neo4jRetriever:
    def __init__(self, uri: str, user: str, password: str):
        self.db = os.getenv("NEO4J_DB", "neo4j")
        self.ready = False
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            with self.driver.session(database=self.db) as s:
                s.run("RETURN 1").consume()
            self.ready = True
            print("[NEO4J] connected OK")
        except Exception as e:
            print("[NEO4J] init error:", e)

    # ---------- Title-first search (returns full articles) ----------
    def search_articles_and_decrees_by_title(
        self,
        question: str,
        lang: str = "VN",
        limit_total: int = 10,
        must_terms: List[str] = None,
        prefer_terms: List[str] = None
    ) -> Tuple[List[Dict], List[Dict]]:
        if not self.ready:
            return [], []

        render_lang = lang
        # dịch sang VN để search
        if lang == "JP":
            try:
                question = translator.translate(question, src="ja", dest="vi").text
            except Exception as e:
                print("[Translate] JP→VN failed:", e)

        q = (question or "").lower()
        toks = [w for w in q.replace("/", " ").replace("-", " ").split() if len(w) >= 3][:25]
        must_terms   = [t.lower() for t in (must_terms or [])]
        prefer_terms = [t.lower() for t in (prefer_terms or [])]

        cy_law = """
        MATCH (a)
        WHERE ANY(x IN labels(a) WHERE x IN $article_labels)
        OPTIONAL MATCH (l)-[:LAW_HAS_ARTICLE]->(a)
        WITH a, l
        WHERE l IS NULL OR ANY(x IN labels(l) WHERE x IN $law_labels)

        OPTIONAL MATCH (a)-[:HAS_CLAUSE]->(c)
        WITH a, l, collect(c) AS clauses

        RETURN
          'LAW' AS source,
          l.LAW_ID           AS law_id,
          l.NAME_VN          AS law_name_vn,
          l.NAME_EN          AS law_name_en,
          l.NAME_JP          AS law_name_jp,
          l.LINK             AS law_link,

          a.ARTICLE_ID       AS article_id,
          a.NUMBER           AS article_number,
          a.TITLE_VN         AS article_title_vn,
          a.TITLE_EN         AS article_title_en,
          a.TITLE_JP         AS article_title_jp,

          [cl IN clauses | {
            clause_id: cl.CLAUSE_ID,
            number:    cl.NUMBER,
            text_vn:   cl.TEXT_VN,
            text_en:   cl.TEXT_EN,
            text_jp:   cl.TEXT_JP
          }] AS clause_list
        """

        cy_dec = """
        MATCH (a)
        WHERE ANY(x IN labels(a) WHERE x IN $article_labels)
        OPTIONAL MATCH (d)-[:DECREE_HAS_ARTICLE]->(a)
        WITH a, d
        WHERE d IS NULL OR ANY(x IN labels(d) WHERE x IN $decree_labels)

        OPTIONAL MATCH (a)-[:HAS_CLAUSE]->(c)
        WITH a, d, collect(c) AS clauses

        RETURN
          'DECREE' AS source,
          d.DECREE_ID        AS decree_id,
          d.NAME_VN          AS decree_name_vn,
          d.NAME_EN          AS decree_name_en,
          d.NAME_JP          AS decree_name_jp,
          d.LINK             AS decree_link,

          a.ARTICLE_ID       AS article_id,
          a.NUMBER           AS article_number,
          a.TITLE_VN         AS article_title_vn,
          a.TITLE_EN         AS article_title_en,
          a.TITLE_JP         AS article_title_jp,

          [cl IN clauses | {
            clause_id: cl.CLAUSE_ID,
            number:    cl.NUMBER,
            text_vn:   cl.TEXT_VN,
            text_en:   cl.TEXT_EN,
            text_jp:   cl.TEXT_JP
          }] AS clause_list
        """

        try:
            with self.driver.session(database=self.db) as s:
                rows1 = s.run(cy_law, article_labels=ARTICLE_LABELS, law_labels=LAW_LABELS).data()
                rows2 = s.run(cy_dec, article_labels=ARTICLE_LABELS, decree_labels=DECREE_LABELS).data()
        except Exception as e:
            print("[NEO4J] search_by_title error:", e)
            return [], []

        def title_text(r: Dict) -> str:
            t = (r.get("article_title_vn") or "") + " " + (r.get("article_title_en") or "") + " " + (r.get("article_title_jp") or "")
            return t.lower()

        def score_row(r: Dict) -> int:
            title = title_text(r)
            sc = 0
            if must_terms and not all(m in title for m in must_terms):
                return -9999
            sc += 20 * len(must_terms or [])
            sc += sum(3 for p in (prefer_terms or []) if p in title)
            sc += sum(1 for t in toks if t in title)
            return sc

        def build_article(r: Dict) -> Dict:
            title = _pick_title(r, render_lang)
            clauses = []
            for cl in r.get("clause_list") or []:
                clauses.append({
                    "number":  cl.get("number"),
                    "text_vn": cl.get("text_vn"),
                    "text_en": cl.get("text_en"),
                    "text_jp": cl.get("text_jp"),
                    "text":    _resolve_clause_text(cl, render_lang)
                })
            law_obj = {
                "id":      r.get("law_id") or r.get("decree_id"),
                "name_vn": r.get("law_name_vn") or r.get("decree_name_vn"),
                "name_en": r.get("law_name_en") or r.get("decree_name_en"),
                "name_jp": r.get("law_name_jp") or r.get("decree_name_jp"),
                "link":    r.get("law_link")    or r.get("decree_link"),
            }
            return {
                "number":  r.get("article_number"),
                "title":   title,
                "clauses": clauses,
                "law":     law_obj
            }

        rows1 = sorted(rows1, key=score_row, reverse=True)
        rows2 = sorted(rows2, key=score_row, reverse=True)

        law_list    = [build_article(r) for r in rows1 if score_row(r) > -9999][: max(1, limit_total // 2)]
        decree_list = [build_article(r) for r in rows2 if score_row(r) > -9999][: limit_total - len(law_list)]
        return law_list, decree_list

    # ---------- Fallback: search by clause texts ----------
    def search_clauses(
        self,
        question: str,
        topic: str,
        lang: str = "VN",
        limit: int = 8,
        prefer_terms: List[str] = None
    ) -> List[Dict]:
        if not self.ready:
            return []

        render_lang = lang
        if lang == "JP":
            try:
                question = translator.translate(question, src="ja", dest="vi").text
            except Exception as e:
                print("[Translate] JP→VN failed:", e)

        q = (question or "").lower()
        toks = [w for w in q.replace("/", " ").replace("-", " ").split() if len(w) >= 3][:20]
        prefer_terms = [t.lower() for t in (prefer_terms or [])]

        cy = """
        MATCH (a)
        WHERE ANY(x IN labels(a) WHERE x IN $article_labels)
        MATCH (a)-[:HAS_CLAUSE]->(c)
        WHERE ANY(x IN labels(c) WHERE x IN $clause_labels)
        OPTIONAL MATCH (l)-[:LAW_HAS_ARTICLE]->(a)
        WITH a, c, l
        OPTIONAL MATCH (d)-[:DECREE_HAS_ARTICLE]->(a)
        WITH a, c, l, d,
             coalesce(l.LINK, d.LINK)      AS link,
             coalesce(l.LAW_ID, d.DECREE_ID) AS pid,
             coalesce(l.NAME_VN, d.NAME_VN) AS pvn,
             coalesce(l.NAME_EN, d.NAME_EN) AS pen,
             coalesce(l.NAME_JP, d.NAME_JP) AS pjp
        RETURN a, c, pid, pvn, pen, pjp, link
        """
        try:
            with self.driver.session(database=self.db) as s:
                rows = s.run(
                    cy,
                    law_labels=LAW_LABELS, decree_labels=DECREE_LABELS,
                    article_labels=ARTICLE_LABELS, clause_labels=CLAUSE_LABELS
                ).data()
        except Exception as e:
            print("[NEO4J] search_clauses error:", e)
            return []

        def clause_text(cl: Dict) -> str:
            t = (cl.get("TEXT_VN") or "") + " " + (cl.get("TEXT_EN") or "") + " " + (cl.get("TEXT_JP") or "")
            return t.lower()

        scored: Dict[Any, int] = {}
        tmp_group: Dict[Any, Dict] = {}

        for r in rows:
            a = r["a"]
            c = r["c"]
            aid = a.get("ARTICLE_ID")
            anumber = a.get("NUMBER")
            atitle_vn = a.get("TITLE_VN")
            atitle_en = a.get("TITLE_EN")
            atitle_jp = a.get("TITLE_JP")

            t = clause_text(c)
            sc = 0
            sc += sum(3 for p in prefer_terms if p in t)
            sc += sum(1 for tok in toks if tok in t)
            if sc == 0:
                continue

            scored[aid] = scored.get(aid, 0) + sc
            if aid not in tmp_group:
                tmp_group[aid] = {
                    "number": anumber,
                    "title": _pick_title({
                        "article_title_vn": atitle_vn,
                        "article_title_en": atitle_en,
                        "article_title_jp": atitle_jp,
                        "law_name_vn": r.get("pvn"),
                        "law_name_en": r.get("pen"),
                        "law_name_jp": r.get("pjp"),
                    }, render_lang),
                    "clauses": [],
                    "law": {
                        "id": r.get("pid"),
                        "name_vn": r.get("pvn"),
                        "name_en": r.get("pen"),
                        "name_jp": r.get("pjp"),
                        "link": r.get("link"),
                    }
                }
            tmp_group[aid]["clauses"].append({
                "number":  c.get("NUMBER"),
                "text_vn": c.get("TEXT_VN"),
                "text_en": c.get("TEXT_EN"),
                "text_jp": c.get("TEXT_JP"),
                "text":    _resolve_clause_text({
                    "text_vn": c.get("TEXT_VN"),
                    "text_en": c.get("TEXT_EN"),
                    "text_jp": c.get("TEXT_JP"),
                }, render_lang),
            })

        aids_sorted = sorted(scored.keys(), key=lambda k: scored[k], reverse=True)[:limit]
        return [tmp_group[aid] for aid in aids_sorted]

    # ---------- Lawyers ----------
    def search_lawyers(self, topic: str, lang: str = "VN", limit: int = 3) -> List[Dict]:
        if not self.ready:
            return []

        render_lang = lang
        if lang == "JP":
            try:
                topic = translator.translate(topic, src="ja", dest="vi").text
            except Exception as e:
                print("[Translate] JP→VN failed:", e)

        t = (topic or "").lower()
        kws = []
        if "trademark" in t or "nhãn hiệu" in t or "thuong hieu" in t: kws += ["trademark", "nhãn hiệu", "thuong hieu", "mark"]
        if "copyright" in t or "bản quyền" in t or "ban quyen" in t or "quyền tác giả" in t: kws += ["copyright", "bản quyền", "ban quyen"]
        if "patent" in t or "sáng chế" in t or "sang che" in t: kws += ["patent", "sáng chế", "sang che"]
        if "design" in t or "kiểu dáng" in t or "kieu dang" in t: kws += ["design", "kiểu dáng", "kieu dang"]
        if not kws: kws = ["ip", "intellectual", "so huu tri tue"]

        cy = """
        MATCH (lw)
        WHERE ANY(x IN labels(lw) WHERE x IN $lawyer_labels)
          AND (
               ANY(k IN $kws WHERE
                    toLower(coalesce(lw.SPECIALTY_EN, "")) CONTAINS k OR
                    toLower(coalesce(lw.SPECIALTY_VN, "")) CONTAINS k OR
                    toLower(coalesce(lw.SPECIALTY_JP, "")) CONTAINS k OR
                    toLower(coalesce(lw.NAME_EN, ""))      CONTAINS k OR
                    toLower(coalesce(lw.NAME_VN, ""))      CONTAINS k OR
                    toLower(coalesce(lw.NAME_JP, ""))      CONTAINS k OR
                    toLower(coalesce(lw.FIRM_EN, ""))      CONTAINS k OR
                    toLower(coalesce(lw.FIRM_VN, ""))      CONTAINS k OR
                    toLower(coalesce(lw.FIRM_JP, ""))      CONTAINS k
               )
               OR
               (lw.SPECIALTY_EN IS NOT NULL OR lw.SPECIALTY_VN IS NOT NULL OR lw.SPECIALTY_JP IS NOT NULL)
          )
        RETURN
            lw.LAWYER_ID        AS id,
            lw.NAME_VN          AS name_vn,
            lw.NAME_EN          AS name_en,
            lw.NAME_JP          AS name_jp,
            lw.FIRM_VN          AS firm_vn,
            lw.FIRM_EN          AS firm_en,
            lw.FIRM_JP          AS firm_jp,
            lw.SPECIALTY_VN     AS spec_vn,
            lw.SPECIALTY_EN     AS spec_en,
            lw.SPECIALTY_JP     AS spec_jp,
            lw.EMAIL            AS email,
            lw.TELEPHONE_NUMBER AS phone
        LIMIT $lim
        """
        try:
            with self.driver.session(database=self.db) as s:
                rows = s.run(cy, kws=[k.lower() for k in kws], lim=limit, lawyer_labels=LAWYER_LABELS).data()
        except Exception as e:
            print("[NEO4J] search_lawyers error:", e)
            rows = []

        out: List[Dict] = []
        for r in rows:
            if render_lang == "VN":
                name = r.get("name_vn") or r.get("name_en") or r.get("name_jp")
                firm = r.get("firm_vn") or r.get("firm_en") or r.get("firm_jp")
                spec = r.get("spec_vn") or r.get("spec_en") or r.get("spec_jp")
            elif render_lang == "JP":
                name = r.get("name_jp") or r.get("name_en") or r.get("name_vn")
                firm = r.get("firm_jp") or r.get("firm_en") or r.get("firm_vn")
                spec = r.get("spec_jp") or r.get("spec_en") or r.get("spec_vn")
            else:
                name = r.get("name_en") or r.get("name_vn") or r.get("name_jp")
                firm = r.get("firm_en") or r.get("firm_vn") or r.get("firm_jp")
                spec = r.get("spec_en") or r.get("spec_vn") or r.get("spec_jp")

            out.append({
                "id": r.get("id") or "",
                "name": name,
                "office": firm,
                "specialty": spec,
                "rating": 4.8,
                "cases": 12,
                "email": r.get("email") or "",
                "phone": r.get("phone") or ""
            })
        return out
