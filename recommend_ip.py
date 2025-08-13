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

def load_lawyers_from_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    combined = []
    for _, r in df.iterrows():
        parts = [
            str(r.get("SPECIALTY_EN", "")),
            str(r.get("SPECIALTY_VN", "")),
            str(r.get("SPECIALTY_JP", "")),
        ]
        combined.append(" \n".join([p for p in parts if p and p != "nan"]))
    df["_combined_text"] = combined
    return df

def load_lawyers_from_neo4j() -> pd.DataFrame:
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    q = """
        MATCH (lw:Lawyer)
        RETURN lw.LAWYER_ID AS LAWYER_ID, lw.NAME_EN AS NAME_EN, lw.NAME_VN AS NAME_VN, lw.NAME_JP AS NAME_JP,
               lw.FIRM AS FIRM, lw.SPECIALTY_EN AS SPECIALTY_EN, lw.SPECIALTY_VN AS SPECIALTY_VN,
               lw.SPECIALTY_JP AS SPECIALTY_JP, lw.contact AS CONTACT
    """
    with driver.session() as s:
        rows = [r.data() for r in s.run(q)]
    df = pd.DataFrame(rows)
    if df.empty:
        raise SystemExit("No lawyers found in Neo4j.")
    df["_combined_text"] = (
        df["SPECIALTY_EN"].fillna("") + " \n" +
        df["SPECIALTY_VN"].fillna("") + " \n" +
        df["SPECIALTY_JP"].fillna("")
    )
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
    ap = argparse.ArgumentParser(description="Recommend IP lawyers by semantic similarity")
    ap.add_argument("query", type=str, help="Short description of the issue (EN/JP/VN)")
    ap.add_argument("--top-k", type=int, default=5)
    args = ap.parse_args()

    result, df = recommend(args.query, args.top_k)
    print("Top matches:\n")
    for i, score in result:
        row = df.iloc[i]
        print(f"- {row.get('NAME_EN', row.get('NAME_VN', 'Unknown'))} | {row.get('FIRM','')} | score={score:.3f}")
        print(f"  Specialty(EN): {row.get('SPECIALTY_EN','')}")
        print(f"  Contact: {row.get('CONTACT','')}")
        print()

if __name__ == "__main__":
    main()
