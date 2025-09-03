# LawIP – Legal Knowledge Graph Chatbot  

## 📌 Giới thiệu  
**LawIP** là một hệ thống chatbot luật Sở hữu trí tuệ (Intellectual Property) dành cho người Nhật sống và làm việc tại Việt Nam.  
Dự án kết hợp **Neo4j (graph database)** với **FastAPI backend** và **React frontend** để:  

- Trả lời câu hỏi liên quan đến Luật SHTT Việt Nam (RAG – Retrieval Augmented Generation).  
- Trích xuất dữ liệu từ cơ sở dữ liệu luật (Law, Decree, Article, Clause).  
- Gợi ý luật sư phù hợp dựa trên lĩnh vực chuyên môn.  

⚠️ Hiện tại: Project mới chạy **local** (chưa deploy được).  

---

## 🏗️ Kiến trúc hệ thống  

```
┌───────────┐      REST API      ┌──────────┐      HTTP      ┌────────────┐
│   Neo4j   │◄──────────────────►│ FastAPI  │◄──────────────►│   React    │
│ Graph DB  │      Cypher        │ Backend  │    JSON        │ Frontend   │
└───────────┘                    └──────────┘                └────────────┘
```

- **Neo4j**: Lưu trữ dữ liệu luật (Law, Decree, Article, Clause, Lawyer, Case, User).  
- **FastAPI**: Xử lý API, kết nối Neo4j, chạy RAG cho chatbot.  
- **React**: Giao diện người dùng (chatbot + tra cứu luật + profile luật sư).  

---

## 🚀 Cách chạy local  

### 1. Cài đặt Neo4j  
- Tải [Neo4j Desktop](https://neo4j.com/download/) hoặc chạy Docker.  
- Tạo database mới, import CSV (`Law.csv`, `Decree.csv`, `Article.csv`, `Clause.csv`, `Lawyer.csv`).  
- Tạo index và constraint bằng file `all.cypher`.  

### 2. Chạy Backend (FastAPI)  

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate   # Windows
source .venv/bin/activate # Linux/Mac

pip install -r requirements.txt
uvicorn app.main:app --reload
```

API chạy tại: `http://127.0.0.1:8000`  

### 3. Chạy Frontend (React)  

```bash
cd my-app
npm install
npm install react-icons
npm run dev
```

Frontend chạy tại: `http://localhost:5173`  

---

## 🛠️ Công nghệ sử dụng  

- **Neo4j**: Graph database (Knowledge Graph cho luật SHTT).  
- **FastAPI**: Backend API (Python).  
- **React + Vite**: Frontend.  
- **LangChain (dự kiến)**: Tích hợp RAG với LLM để chatbot trả lời tự nhiên hơn.  

---

