# -*- coding: utf-8 -*-
import os, json, unicodedata

BASE_DIR = os.path.dirname(__file__)
MAP_PATH = os.path.join(BASE_DIR, "intent_title_map.json")

try:
    with open(MAP_PATH, "r", encoding="utf-8") as f:
        INTENT_MAP = json.load(f)
except Exception:
    INTENT_MAP = {}

def _strip_accents(s: str) -> str:
    s = s or ""
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower()

def _has_any(t: str, words):
    t0 = _strip_accents(t)
    return any(_strip_accents(w) in t0 for w in words)

def detect_intent(text: str) -> str:
    if _has_any(text, ["bản quyền", "ban quyen", "copyright", "tác giả", "tac gia"]):
        if _has_any(text, ["đăng ký", "dang ky", "register", "hồ sơ", "nop don", "nộp đơn"]):
            return "copyright_register"
        if _has_any(text, ["xâm phạm", "xam pham", "sao chép", "copy", "infring"]):
            return "copyright_infringe"
        return "copyright_generic"
    if _has_any(text, ["nhãn hiệu", "thuong hieu", "trademark", "logo"]):
        if _has_any(text, ["đăng ký", "dang ky", "register", "hồ sơ", "nộp đơn", "nop don"]):
            return "trademark_register"
        if _has_any(text, ["xâm phạm", "xam pham", "giả mạo", "copy", "infring"]):
            return "trademark_infringe"
        return "trademark_generic"
    if _has_any(text, ["sáng chế", "sang che", "patent"]):
        return "patent_generic"
    if _has_any(text, ["kiểu dáng", "kieu dang", "industrial design"]):
        return "design_generic"
    return "generic"

def title_keywords_for_intent(intent: str):
    block = INTENT_MAP.get(intent, {})
    items = block.get("law_titles", []) + block.get("decree_titles", []) + block.get("extra_kw", [])
    out = []
    seen = set()
    for k in items:
        for z in (k.lower(), _strip_accents(k)):
            if z and z not in seen:
                seen.add(z); out.append(z)
    return out
