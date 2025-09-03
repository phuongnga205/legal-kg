# -*- coding: utf-8 -*-
import re

# 12 nhóm chủ đề lớn
TOPIC_KEYWORDS = {
    "trademark": [
        r"\bnhãn ?hiệu\b", r"\bthương ?hiệu\b", r"\blogo\b", r"\bbrand\b",
        r"\btrademark\b", r"商標", r"ロゴ", r"ブランド", r"counterfeit", r"fake"
    ],
    "copyright": [
        r"\bbản ?quyền\b", r"\bquyền tác giả\b", r"\bin lậu\b", r"\bsao chép\b",
        r"\bcopyright\b", r"著作権", r"海賊版", r"pirate", r"pirated"
    ],
    "patent": [
        r"\bsáng ?chế\b", r"\bphát minh\b", r"\bgiải pháp hữu ích\b",
        r"\bpatent\b", r"特許", r"発明"
    ],
    "design": [
        r"\bkiểu ?dáng\b", r"\bmẫu mã\b", r"\bindustrial design\b",
        r"\bdesign\b", r"意匠"
    ],
    "gi": [
        r"\bchỉ dẫn địa lý\b", r"\bgeographical indication\b", r"\bGI\b",
        r"地理的表示"
    ],
    "license": [
        r"\bchuyển nhượng\b", r"\bcấp phép\b", r"\blis?ense\b", r"\bhợp đồng\b",
        r"契約", r"ライセンス"
    ],
    "trade_secrets": [
        r"\bbí mật kinh doanh\b", r"\btrade secrets?\b", r"営業秘密", r"\bNDA\b"
    ],
    "enforcement": [
        r"\bxử lý vi phạm\b", r"\bkhởi kiện\b", r"\bchế tài\b",
        r"\benhancement\b", r"\benforcement\b", r"差止", r"制裁"
    ],
    "domain_names": [
        r"\btên miền\b", r"\bdomain\b", r"\bcybersquatt\w*\b"
    ],
    "ip_customs": [
        r"\bhải quan\b", r"\bbiên giới\b", r"\bcustoms\b", r"税関"
    ],
    "plant_varieties": [
        r"\bgiống cây trồng\b", r"\bplant varieties\b", r"PVP", r"DUS"
    ],
    "ic_layout": [
        r"\bbố trí mạch\b", r"\bIC layout\b", r"\blayout design\b",
        r"回路配置", r"半導体"
    ],
}

# fallback
DEFAULT_TOPIC = "dispute"

def detect_topic(text: str) -> str:
    if not text:
        return DEFAULT_TOPIC
    low = text.lower()
    for topic, patterns in TOPIC_KEYWORDS.items():
        for pat in patterns:
            if re.search(pat, low, flags=re.IGNORECASE):
                return topic
    return DEFAULT_TOPIC
