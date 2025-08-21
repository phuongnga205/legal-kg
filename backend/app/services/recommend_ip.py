# recommend_ip.py
import os
import argparse
import numpy as np
import pandas as pd
from typing import List, Tuple
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from neo4j import GraphDatabase

# Load config
load_dotenv()
EMBED_MODEL = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
LAWYERS_CSV = os.getenv("LAWYERS_CSV", "./data/lawyer.csv")
LAWYERS_FROM_NEO4J = os.getenv("LAWYERS_FROM_NEO4J", "false").lower() == "true"

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "neo4j")

# Load embedding model
model = SentenceTransformer(EMBED_MODEL)

def _combine_specialty(row: pd.Series) -> str:
    parts = [
        str(row.get("SPECIALTY_EN", "") or ""),
        str(row.get("SPECIALTY_VN", "") or ""),
        str(row.get("SPECIALTY_JP", "") or ""),
    ]
    return " \n".join([p for p in parts if p.strip() and p.lower() != "nan"])

def load_lawyers_from_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # Chuẩn hoá cột tên nếu viết khác (FIRM vs FIRM_EN/VN/JP; CONTACT vs EMAIL/TELEPHONE NUMBER)
    if "FIRM" not in df.columns:
        # Nếu có FIRM_EN/VN/JP thì tạo cột FIRM (EN ưu tiên → VN → JP)
        df["FIRM"] = df.get("FIRM_EN", "").fillna("").where(df.get("FIRM_EN", "").notna(),
                     df.get("FIRM_VN", "").fillna("").where(df.get("FIRM_VN", "").notna(),
                     df.get("FIRM_JP", "").fillna("")))
    # CONTACT: gộp EMAIL + TELEPHONE NUMBER (nếu có)
    if "CONTACT" not in df.columns:
        tel = df.get("TELEPHONE NUMBER", "") if "TELEPHONE NUMBER" in df.columns else df.get("TELEPHONE_NUMBER", "")
        tel = tel.fillna("")
        email = df.get("EMAIL", "").fillna("")
        df["CONTACT"] = (("Tel: " + tel).str.strip() + " | Email: " + email).str.strip(" |")

    df["_combined_text"] = df.apply(_combine_specialty, axis=1)
    return df

def load_lawyers_from_neo4j() -> pd.DataFrame:
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    # Lấy đủ cột theo schema. Với cột có dấu cách, dùng backtick.
    q = """
        MATCH (lw:Lawyer)
        RETURN
          lw.LAWYER_ID        AS LAWYER_ID,
          lw.NAME_EN          AS NAME_EN,
          lw.NAME_VN          AS NAME_VN,
          lw.NAME_JP          AS NAME_JP,
          coalesce(lw.FIRM_EN, lw.FIRM_VN, lw.FIRM_JP, lw.FIRM) AS FIRM,
          lw.SPECIALTY_EN     AS SPECIALTY_EN,
          lw.SPECIALTY_VN     AS SPECIALTY_VN,
          lw.SPECIALTY_JP     AS SPECIALTY_JP,
          coalesce(lw.EMAIL, '') AS EMAIL,
          coalesce(lw.`TELEPHONE NUMBER`, lw.TELEPHONE_NUMBER, '') AS TELEPHONE
    """
    with driver.session() as s:
        rows = [r.data() for r in s.run(q)]
    df = pd.DataFrame(rows)
    if df.empty:
        raise SystemExit("No lawyers found in Neo4j.")
    df["_combined_text"] = df.apply(_combine_specialty, axis=1)
    df["CONTACT"] = (("Tel: " + df["TELEPHONE"].fillna("")) + " | Email: " + df["EMAIL"].fillna("")).str.strip(" |")
    return df

def embed_texts(texts: List[str]) -> np.ndarray:
    embs = model.encode(texts, normalize_embeddings=True)
    return np.array(embs)

def recommend(query: str, top_k: int = 5) -> Tuple[List[Tuple[int, float]], pd.DataFrame]:
    if LAWYERS_FROM_NEO4J:
        df = load_lawyers_from_neo4j()
    else:
        df = load_lawyers_from_csv(LAWYERS_CSV)

    if df.empty:
        return [], df

    lawyer_embs = embed_texts(df["_combined_text"].tolist())
    query_emb = embed_texts([query])[0]

    scores = lawyer_embs @ query_emb
    idx = np.argsort(-scores)[:top_k]
    return [(int(i), float(scores[i])) for i in idx], df

def main():
    ap = argparse.ArgumentParser(description="Recommend IP lawyers (aligned with LAWYER schema)")
    ap.add_argument("query", type=str, help="Short description of the issue (EN/JP/VN)")
    ap.add_argument("--top-k", type=int, default=5)
    args = ap.parse_args()

    result, df = recommend(args.query, args.top_k)
    print("Top matches:\n")
    for i, score in result:
        row = df.iloc[i]
        display_name = row.get("NAME_EN") or row.get("NAME_VN") or row.get("NAME_JP") or "Unknown"
        print(f"- {display_name} | {row.get('FIRM','')} | score={score:.3f}")
        print(f"  Specialty(EN): {row.get('SPECIALTY_EN','')}")
        if row.get("EMAIL") or row.get("TELEPHONE") or row.get("CONTACT"):
            print(f"  Contact: {row.get('CONTACT', '')}")
        print()

if __name__ == "__main__":
    main()
