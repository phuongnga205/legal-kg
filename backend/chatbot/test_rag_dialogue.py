# chatbot/test_rag_dialogue.py
# -*- coding: utf-8 -*-

from dialogue_manager import (
    make_advice, reset_state, get_state,
    detect_lang_auto, update_registered_state
)
from retriever_neo4j import Neo4jRetriever

def header_line(r, lang="VN"):
    art = r["article_number"]
    cl  = r["clause_number"]
    name = r["law_name"] or "Văn bản pháp luật"

    if lang == "EN":
        if cl and cl != 0:
            return f"👉 {name} - Article {art} Clause {cl}"
        else:
            return f"👉 {name} - Article {art}"
    elif lang == "JP":
        if cl and cl != 0:
            return f"👉 {name} - 第{art}条 第{cl}項"
        else:
            return f"👉 {name} - 第{art}条"
    else:  # VN
        if cl and cl != 0:
            return f"👉 {name} - Điều {art} Khoản {cl}"
        else:
            return f"👉 {name} - Điều {art}"

def law_title(lang):
    return {
        "EN": "📖 According to the law:",
        "JP": "📖 法令の該当条文:",
    }.get(lang, "📖 Theo luật:")

def link_title(lang):
    return {
        "EN": "📎 Source:",
        "JP": "📎 出典:",
    }.get(lang, "📎 Nguồn:")

def lawyer_line(lang, name):
    return {
        "EN": f"⚖️ You may consult: {name}",
        "JP": f"⚖️ ご相談先の弁護士: {name}",
    }.get(lang, f"⚖️ Bạn có thể tham khảo luật sư: {name}")

if __name__ == "__main__":
    print("=== Test Chatbot RAG + Neo4j (VN/EN/JP) ===")
    reset_state()
    retriever = Neo4jRetriever()

    try:
        while True:
            q = input("Q: ").strip()
            if not q:
                break

            # 1) detect language + cập nhật slot nếu user trả lời 'có/không/chưa/yes/no'
            lang = detect_lang_auto(q)
            _ = update_registered_state(q)

            # 2) sinh advice theo state/topic
            advice = make_advice(q, lang=lang)

            # 3) truy hồi clause thật từ Neo4j (full-text)
            results = retriever.search_clauses(q, lang=lang, limit=3)

            # 4) in ra
            print("A:", advice, "\n")
            print(law_title(lang))
            if not results:
                print({"EN": "No relevant clause found.", "JP": "該当条文が見つかりません。"}
                      .get(lang, "Không tìm thấy điều luật liên quan."))
            else:
                links = []
                for r in results:
                    print(header_line(r, lang))
                    print(r.get("clause_text", "").strip())
                    if r.get("law_link"):
                        links.append(r["law_link"])
                # gom link (unique) và in 1 lần ở CUỐI
                uniq = []
                for L in links:
                    if L and L not in uniq:
                        uniq.append(L)
                if uniq:
                    print(link_title(lang), "; ".join(uniq))

            # 5) gợi ý luật sư (mock)
            lawyer = "Nguyễn Văn A" if lang == "VN" else ("Anna Nguyen" if lang == "EN" else "田中一郎")
            print("\n" + lawyer_line(lang, lawyer) + "\n")

    finally:
        retriever.close()
