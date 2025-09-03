# -*- coding: utf-8 -*-
from typing import Optional, Dict
import unicodedata, re

_state: Dict[str, Optional[bool]] = {"topic": None, "registered": None}

def reset_state():
    global _state
    _state = {"topic": None, "registered": None}

def get_state() -> Dict[str, Optional[bool]]:
    return dict(_state)

def set_state(new_state: Dict[str, Optional[bool]]):
    global _state
    _state = {"topic": new_state.get("topic"), "registered": new_state.get("registered")}

def _strip_accents(s: str) -> str:
    if not s: return s
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")

def detect_lang_auto(text: str) -> str:
    if not text: return "VN"
    jp_hint = sum(1 for ch in text if (0x3040 <= ord(ch) <= 0x30FF or 0x4E00 <= ord(ch) <= 0x9FFF))
    if jp_hint >= 2: return "JP"
    en_tokens = {"the","and","you","trademark","copyright","patent","logo","brand","domain","license"}
    low = (text or "").lower()
    if any(t in low for t in en_tokens): return "EN"
    return "VN"

def _has(q: str, words) -> bool:
    return any(w in q for w in words)

# ---- topic detector: bao phủ “copy nhãn hiệu”, “đăng ký bản quyền”, ...
def detect_topic(question: str) -> Optional[str]:
    q = (question or "").lower()
    # trademark (mọi biến thể “copy/nhái/sao chép + nhãn hiệu/thương hiệu/logo”)
    if (_has(q, ["nhãn hiệu","thương hiệu","logo","brand","trademark"]) and
        _has(q, ["copy","sao chép","nhái","làm giả","xâm phạm","vi phạm","dùng trái phép","infring"])):
        return "trademark"
    if _has(q, ["nhãn hiệu","thương hiệu","logo","brand","trademark"]):
        return "trademark"

    # copyright
    if (_has(q, ["bản quyền","quyền tác giả","copyright"]) or
        (_has(q, ["copy","sao chép"]) and _has(q, ["tác phẩm","bài viết","hình ảnh","video","nhạc","music","work","content"]))):
        return "copyright"

    # patent / design / trade secrets / license / GI / enforcement / domain / plant varieties / IC layout
    if _has(q, ["sáng chế","phát minh","patent","invention"]): return "patent"
    if _has(q, ["kiểu dáng","industrial design","design công nghiệp"]): return "design"
    if _has(q, ["bí mật kinh doanh","trade secret"]): return "trade_secrets"
    if _has(q, ["cấp phép","license","licensing","chuyển nhượng","assign"]): return "license"
    if _has(q, ["chỉ dẫn địa lý","geographical indication"," gi "]): return "gi"
    if _has(q, ["vi phạm","tranh chấp","khởi kiện","enforcement","sue","litigation"]): return "enforcement"
    if _has(q, ["tên miền","domain","udrp","cybersquat"]): return "domain_names"
    if _has(q, ["giống cây","plant variety","pvp"]): return "plant_varieties"
    if _has(q, ["bố trí mạch","ic layout","circuit layout"]): return "ic_layout"
    return None

# ---- hiểu “đã/chưa đăng ký” cả câu dài (VN/EN/JP)
def update_registered_state(answer_text: str) -> Optional[bool]:
    global _state
    if not answer_text: return None
    a = answer_text.strip().lower()
    a_no_acc = _strip_accents(a)

    # JP ngắn
    if a in {"はい"}: _state["registered"] = True; return True
    if a in {"いいえ"}: _state["registered"] = False; return False

    # yes/no siêu ngắn
    if len(a_no_acc) <= 4:
        if a_no_acc in {"co","có","da","roi","rồi","yes","y"}:
            _state["registered"] = True; return True
        if a_no_acc in {"khong","không","chua","chưa","no","n"}:
            _state["registered"] = False; return False

    # Câu dài (regex)
    neg_then_action = re.search(r"\b(chua|chưa|khong|không|not|no)\b.*\b(dang|đăng|register|file|apply)", a_no_acc)
    pos_then_action = re.search(r"\b(da|đã|roi|rồi|already|have|registered)\b.*\b(dang|đăng|register|file|apply)", a_no_acc)
    if neg_then_action:
        _state["registered"] = False; return False
    if pos_then_action:
        _state["registered"] = True; return True

    return None

def make_advice(question: str, lang: Optional[str] = None) -> str:
    global _state
    lang = lang or detect_lang_auto(question)
    topic = detect_topic(question) or _state.get("topic")
    _state["topic"] = topic

    # Hỏi lại cho trademark & copyright
    if topic == "trademark":
        if _state["registered"] is None:
            return "Bạn đã đăng ký nhãn hiệu này chưa?"
        elif _state["registered"] is False:
            return "🔑 Lời khuyên: Hãy chuẩn bị hồ sơ và đăng ký nhãn hiệu tại Cục SHTT. Vui lòng đọc kỹ các điều luật bên dưới để đảm bảo quyền lợi."
        else:
            return "🔑 Lời khuyên: Nếu đã đăng ký, bạn có thể yêu cầu xử lý vi phạm, khiếu nại hoặc khởi kiện. Vui lòng đọc kỹ các điều luật bên dưới để đảm bảo quyền lợi."

    if topic == "copyright":
        if _state["registered"] is None:
            return "Bạn đã đăng ký quyền tác giả cho tác phẩm này chưa?"
        elif _state["registered"] is False:
            return "🔑 Lời khuyên: Hãy đăng ký bản quyền và giữ bản gốc làm chứng cứ. Xem các điều luật gợi ý bên dưới."
        else:
            return "🔑 Lời khuyên: Với bản quyền đã đăng ký, bạn có thể yêu cầu xử lý/khởi kiện. Xem điều luật bên dưới."

    # Các topic khác: đưa khuyến nghị ngay (router sẽ chủ động truy vấn điều luật)
    if topic == "patent":
        return "🔑 Lời khuyên: Tra cứu tính mới, chuẩn bị bản mô tả sáng chế và nộp đơn."
    if topic == "design":
        return "🔑 Lời khuyên: Đăng ký kiểu dáng công nghiệp; nếu bị sao chép, chuẩn bị chứng cứ."
    if topic == "enforcement":
        return "🔑 Lời khuyên: Cân nhắc biện pháp hành chính, dân sự, hình sự; chuẩn bị chứng cứ."
    if topic == "domain_names":
        return "🔑 Lời khuyên: Thu thập chứng cứ chiếm dụng tên miền và xem thủ tục giải quyết tranh chấp."

    return "🔑 Lời khuyên chung: Thu thập chứng cứ, chuẩn bị hồ sơ pháp lý và liên hệ cơ quan có thẩm quyền."
