# chatbot/rag_bot.py
from retriever_neo4j import Neo4jRetriever
from dialogue_manager import (
    detect_language_simple,
    detect_topic,
    make_advice,
    update_registered_state,
    reset_state,
)

import random

# Một ít anchor cho full-text theo topic (đủ xài; muốn mạnh hơn thì mở rộng thêm)
TOPIC_FT = {
    "trademark": {
        "VN": 'nhãn hiệu OR "tương tự gây nhầm lẫn" OR "xâm phạm nhãn hiệu"',
        "EN": 'trademark OR "confusingly similar" OR "trademark infringement"',
        "JP": '商標 OR 混同 OR 侵害',
    },
    "copyright": {
        "VN": 'bản quyền OR "quyền tác giả" OR "sao chép" OR "in lậu"',
        "EN": 'copyright OR "copyright infringement" OR pirated OR copy',
        "JP": '著作権 OR 侵害 OR 海賊版',
    },
    "patent": {
        "VN": 'sáng chế OR phát minh OR "xâm phạm sáng chế"',
        "EN": 'patent OR invention OR "patent infringement"',
        "JP": '特許 OR 発明 OR 侵害',
    },
    "design": {
        "VN": 'kiểu dáng công nghiệp OR mẫu mã OR "sao chép mẫu mã"',
        "EN": 'industrial design OR design OR copying',
        "JP": '意匠 OR デザイン OR 模倣',
    },
    "gi": {
        "VN": 'chỉ dẫn địa lý OR xuất xứ',
        "EN": 'geographical indication OR origin',
        "JP": '地理的表示 OR 産地',
    },
    "trade_secrets": {
        "VN": 'bí mật kinh doanh OR bảo mật OR NDA',
        "EN": 'trade secret OR confidential OR NDA',
        "JP": '営業秘密 OR 秘密保持',
    },
    "license": {
        "VN": 'chuyển nhượng OR cấp phép OR hợp đồng',
        "EN": 'license OR assignment OR contract',
        "JP": 'ライセンス OR 譲渡 OR 契約',
    },
    "enforcement": {
        "VN": 'xử phạt OR cưỡng chế OR khởi kiện',
        "EN": 'enforcement OR sanction OR lawsuit',
        "JP": '執行 OR 制裁 OR 訴訟',
    },
}

# Tên luật sư demo
LAWYERS = {
    "VN": ["Nguyễn Văn A", "Trần Thị B", "Đặng Thùy Dương", "Lê Thu D"],
    "EN": ["Anna Nguyen", "David Tran", "Hanh Dang"],
    "JP": ["佐藤健", "田中一郎", "鈴木花子"],
}

def _choose_lawyer(lang="VN"):
    arr = LAWYERS.get(lang, LAWYERS["VN"])
    return random.choice(arr)

def _format_clause_line(rec, lang="VN"):
    # Ẩn “Khoản/Clause/第0項”
    law_name = rec.get("law_name") or (
        "Văn bản pháp luật" if lang == "VN" else "Legal text" if lang == "EN" else "法令"
    )
    art = rec.get("article_number")
    cl = rec.get("clause_number")
    text = (rec.get("clause_text") or "").strip()

    if lang == "VN":
        title = f"👉 {law_name} - Điều {art}" + (f" Khoản {cl}" if cl and int(cl) != 0 else "")
        return title + "\n" + text
    elif lang == "EN":
        title = f"👉 {law_name} - Article {art}" + (f" Clause {cl}" if cl and int(cl) != 0 else "")
        return title + "\n" + text
    else:  # JP
        title = f"👉 {law_name} - 第{art}条" + (f" 第{cl}項" if cl and int(cl) != 0 else "")
        return title + "\n" + text

def _build_ft_query(user_text, topic, lang):
    # Nếu có anchor theo topic thì ưu tiên, không thì dùng nguyên câu hỏi
    tmap = TOPIC_FT.get(topic)
    if not tmap:
        return user_text
    return tmap.get(lang, user_text)

class RAGBot:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="BENCHAN2025"):
        self.retriever = Neo4jRetriever(uri, user, password)
        reset_state()

    def close(self):
        self.retriever.close()

    def ask(self, user_text: str):
        # 1) Detect language & topic
        lang = detect_language_simple(user_text)
        topic = detect_topic(user_text)

        # 2) Advice theo dialogue state (slot-based trong dialogue_manager)
        advice = make_advice(user_text, lang)

        # 3) Retriever: full-text theo topic (anchors) + fallback câu user
        ft_q = _build_ft_query(user_text, topic, lang)
        results = self.retriever.search_clauses(ft_q, lang=lang, limit=3)

        # 4) Format clause & gom link về cuối
        body_lines, links = [], []
        for r in results:
            body_lines.append(_format_clause_line(r, lang))
            link = r.get("law_link")
            if link and link not in links:
                links.append(link)

        # 5) Render theo ngôn ngữ
        if lang == "VN":
            law_header = "📖 Theo luật:"
            lawyer_line = f"⚖️ Bạn có thể tham khảo luật sư: {_choose_lawyer('VN')}"
        elif lang == "EN":
            law_header = "📖 According to the law:"
            lawyer_line = f"⚖️ You may consult: {_choose_lawyer('EN')}"
        else:
            law_header = "📖 法令の該当条文:"
            lawyer_line = f"⚖️ ご相談先の弁護士: {_choose_lawyer('JP')}"

        # 6) Lắp ráp
        out = [advice, ""]
        out.append(law_header)
        if body_lines:
            out.extend(body_lines)
            if links:
                out.append("📎 " + " | ".join(links))
        else:
            out.append("Không tìm thấy điều luật liên quan." if lang == "VN" else
                       "No relevant clause found." if lang == "EN" else
                       "該当条文が見つかりませんでした。")

        out.append("")  # dòng trống
        out.append(lawyer_line)
        return "\n".join(out)

    # Dành cho câu trả lời “Có/Chưa/Yes/No/はい/いいえ” để cập nhật slot
    def update_registered(self, user_text: str):
        lang = detect_language_simple(user_text)
        update_registered_state(user_text, lang)
