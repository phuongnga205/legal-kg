import pandas as pd
import random, csv

BASE = "https://raw.githubusercontent.com/phuongnga205/legal-kg/main/data/"
URLS = {
    "law": "https://raw.githubusercontent.com/phuongnga205/legal-kg/main/data/LAW.csv",
    "decree": "https://raw.githubusercontent.com/phuongnga205/legal-kg/main/data/DECREE.csv",
    "article": "https://raw.githubusercontent.com/phuongnga205/legal-kg/main/data/ARTICLE.csv",
    "clause": "https://raw.githubusercontent.com/phuongnga205/legal-kg/main/data/CLAUSE.csv",
    "law_has_article": "https://raw.githubusercontent.com/phuongnga205/legal-kg/main/data/LAW_HAS_ARTICLE.csv",
    "decree_has_article": "https://raw.githubusercontent.com/phuongnga205/legal-kg/main/data/DECREE_HAS_ARTICLE.csv",
    "has_clause": "https://raw.githubusercontent.com/phuongnga205/legal-kg/main/data/HAS_CLAUSE.csv",
    "lawyer": "https://raw.githubusercontent.com/phuongnga205/legal-kg/main/data/LAWYER.csv",
}


# Load CSVs
article_df = pd.read_csv(URLS["article"])
clause_df = pd.read_csv(URLS["clause"])
has_clause_df = pd.read_csv(URLS["has_clause"])
lawyer_df = pd.read_csv(URLS["lawyer"])

for df in [article_df, clause_df, has_clause_df, lawyer_df]:
    df.columns = df.columns.str.strip().str.upper()

# Join Article + Clause
merged = (
    has_clause_df.merge(article_df, on="ARTICLE_ID")
                 .merge(clause_df, on="CLAUSE_ID")
)

print("✅ Tổng số clause:", len(merged))

# Biến thể câu hỏi
TEMPLATES_VN = [
    "Điều {a} Khoản {c} quy định thế nào?",
    "Nội dung Khoản {c} Điều {a} là gì?",
    "Theo luật, Điều {a} Khoản {c} nói gì?",
    "Bạn cho tôi biết chi tiết Khoản {c} trong Điều {a}?",
    "Khoản {c} Điều {a} quy định về vấn đề nào?",
]
TEMPLATES_EN = [
    "What does Article {a}, Clause {c} state?",
    "Tell me the content of Article {a} Clause {c}.",
    "In the law, what is written in Article {a} Clause {c}?",
    "Can you explain Clause {c} of Article {a}?",
    "What issue is covered in Article {a} Clause {c}?",
]
TEMPLATES_JP = [
    "第{a}条 第{c}項には何が規定されていますか？",
    "第{a}条 第{c}項の内容を教えてください。",
    "法律では第{a}条 第{c}項に何が書かれていますか？",
    "第{a}条 第{c}項について説明してください。",
    "第{a}条 第{c}項はどの問題を扱っていますか？",
]

qa_data = []

for _, row in merged.iterrows():
    a_num = row["NUMBER_x"]
    a_title = row.get("TITLE_VN", "")
    c_num = row["NUMBER_y"]
    text_vn = row.get("TEXT_VN", "")
    text_en = row.get("TEXT_EN", "")
    text_jp = row.get("TEXT_JP", "")

    # chọn random luật sư để đề xuất
    lw = lawyer_df.sample(1).iloc[0]

    # câu trả lời gốc
    ans_vn = f"👉 Điều {a_num} - {a_title}, Khoản {c_num}: {text_vn}\n\nĐây chỉ là thông tin tham khảo, vui lòng đọc kỹ luật gốc hoặc liên hệ luật sư.\nBạn có thể tham khảo thêm {lw.get('NAME_VN','Luật sư A')}."
    ans_en = f"👉 Article {a_num} - {a_title}, Clause {c_num}: {text_en}\n\nThis is only reference information, please consult the original law or a lawyer.\nYou may also consult {lw.get('NAME_EN','Lawyer A')}."
    ans_jp = f"👉 第{a_num}条 {a_title}, 第{c_num}項: {text_jp}\n\nこれは参考情報にすぎません。必ず原文または弁護士にご相談ください。\nさらに {lw.get('NAME_JP','弁護士A')} に相談できます。"

    # sinh biến thể
    for t_vn, t_en, t_jp in zip(TEMPLATES_VN, TEMPLATES_EN, TEMPLATES_JP):
        q_vn = t_vn.format(a=a_num, c=c_num)
        q_en = t_en.format(a=a_num, c=c_num)
        q_jp = t_jp.format(a=a_num, c=c_num)
        qa_data.append([q_vn, ans_vn, q_en, ans_en, q_jp, ans_jp])

# Xuất CSV
out_file = "qa_dataset.csv"
with open(out_file, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["QUESTION_VN", "ANSWER_VN", "QUESTION_EN", "ANSWER_EN", "QUESTION_JP", "ANSWER_JP"])
    writer.writerows(qa_data)

print(f"🎉 Saved QA dataset: {out_file}, total {len(qa_data)} samples")
