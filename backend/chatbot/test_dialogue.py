# chatbot/test_dialogue.py
# -*- coding: utf-8 -*-

from dialogue_manager import (
    make_advice, reset_state, get_state,
    detect_lang_auto, update_registered_state, detect_topic
)

print("=== Test Dialogue Manager (Auto Lang Detect) ===")
reset_state()

while True:
    q = input("Q: ").strip()
    if not q:
        break

    lang = detect_lang_auto(q)

    # 1) nếu là câu trả lời ngắn kiểu có/không/chưa → set slot trước
    _ = update_registered_state(q)

    # 2) Debug: hệ thống hiểu gì lúc này
    topic_dbg = detect_topic(q)
    st = get_state()
    print(f"→ Lang: {lang} | Topic: {st.get('topic') or topic_dbg} | Registered: {st.get('registered')}")

    # 3) Sinh advice (giữ topic cũ nếu câu follow-up không có keyword)
    ans = make_advice(q, lang=lang)
    print("A:", ans)
    print("=" * 60)
