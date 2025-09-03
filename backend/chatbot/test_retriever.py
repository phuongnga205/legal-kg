# chatbot/test_retriever.py
from retriever_neo4j import Neo4jRetriever

def print_case(results, lang, header):
    print(f"\nQ: {header}")
    links = []
    for r in results:
        law_name = r.get("law_name") or ("Luật Sở hữu trí tuệ, số 50/2005/QH11" if lang == "VN" else
                                         "Law on Intellectual Property, No. 50/2005/QH11" if lang == "EN" else "知的財産法第50/2005/QH11号")
        art = r.get("article_number")
        cl = r.get("clause_number")
        text = (r.get("clause_text") or "").strip()
        link = r.get("law_link")

        # ----- format tiêu đề theo ngôn ngữ & ẩn khoản 0 -----
        if lang == "VN":
            if cl and int(cl) != 0:
                title = f"👉 {law_name} - Điều {art} Khoản {cl}"
            else:
                title = f"👉 {law_name} - Điều {art}"
        elif lang == "EN":
            if cl and int(cl) != 0:
                title = f"👉 {law_name} - Article {art} Clause {cl}"
            else:
                title = f"👉 {law_name} - Article {art}"
        else:  # JP
            if cl and int(cl) != 0:
                title = f"👉 {law_name} - 第{art}条 第{cl}項"
            else:
                title = f"👉 {law_name} - 第{art}条"

        print(title)
        print(text)

        # Thu thập link (nếu có) để in 1 lần ở cuối, tránh trùng
        if link and link not in links:
            links.append(link)

    if links:
        # In tất cả link một lần cuối (nếu có nhiều luật khác nhau)
        if lang == "VN":
            print("📎 " + " | ".join(links) + "\n")
        elif lang == "EN":
            print("📎 " + " | ".join(links) + "\n")
        else:
            print("📎 " + " | ".join(links) + "\n")

if __name__ == "__main__":
    retriever = Neo4jRetriever()   # giữ nguyên thông số kết nối như bạn đang dùng

    print("=== Test Full-Text Retriever ===")

    # Case 1: Vietnamese trademark
    vn_results = retriever.search_clauses("nhãn hiệu", lang="VN", limit=3)
    print_case(vn_results, "VN", "Tôi bị ăn cắp nhãn hiệu")

    # Case 2: English copyright
    en_results = retriever.search_clauses("copyright", lang="EN", limit=3)
    print_case(en_results, "EN", "Someone copied my book")

    # Case 3: Japanese patent
    jp_results = retriever.search_clauses("特許", lang="JP", limit=3)
    print_case(jp_results, "JP", "私の発明を盗まれた")

    retriever.close()
