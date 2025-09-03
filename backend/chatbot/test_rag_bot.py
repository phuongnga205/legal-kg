# chatbot/test_rag_bot.py
from rag_bot import RAGBot

if __name__ == "__main__":
    bot = RAGBot()

    print("=== Test Chatbot RAG + Neo4j (VN/EN/JP) ===")

    # 1) Trademark – slot-based
    q1 = "Tôi bị ăn cắp nhãn hiệu"
    print(f"Q: {q1}")
    print("A:", bot.ask(q1))
    q2 = "Chưa"
    print(f"\nQ: {q2}")
    bot.update_registered(q2)
    print("A:", bot.ask(q1))  # hỏi lại cùng câu trademark

    # 2) Copyright – slot-based
    q3 = "Ai đó in lậu sách của tôi"
    print(f"\nQ: {q3}")
    print("A:", bot.ask(q3))
    q4 = "Có"
    print(f"\nQ: {q4}")
    bot.update_registered(q4)
    print("A:", bot.ask(q3))

    # 3) EN – trademark
    q5 = "Someone copied my brand logo"
    print(f"\nQ: {q5}")
    print("A:", bot.ask(q5))
    print("\nQ: yes")
    bot.update_registered("yes")
    print("A:", bot.ask(q5))

    # 4) JP – patent
    q6 = "私の発明を盗まれた"
    print(f"\nQ: {q6}")
    print("A:", bot.ask(q6))

    # 5) VN – trade secrets
    q7 = "Bí mật kinh doanh của tôi bị lộ"
    print(f"\nQ: {q7}")
    print("A:", bot.ask(q7))

    bot.close()
