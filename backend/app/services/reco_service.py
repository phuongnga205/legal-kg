from app.services.recommend_ip import recommend

def recommend_lawyers(question: str, lang: str):
    result, df = recommend(question, top_k=3)
    lawyers = []
    for idx, score in result:
        row = df.iloc[idx]
        lawyers.append({
            "NAME": row.get("NAME_EN") or row.get("NAME_VN") or row.get("NAME_JP") or "Unknown",
            "FIRM": row.get("FIRM", ""),
            "SPECIALTY": row.get("SPECIALTY_EN") or row.get("SPECIALTY_VN") or row.get("SPECIALTY_JP"),
            "CONTACT": row.get("CONTACT", ""),
            "SCORE": score,
        })
    return lawyers
