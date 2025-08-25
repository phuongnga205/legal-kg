import { useState, useRef, useEffect } from 'react';
import './ChatBox.css';
import ResultBubble from './ResultBubble';
import ResultOverlay from './ResultOverlay';
const botAvatar = '/bot.png';
const userAvatar = '/user.png';

const getGreeting = (lang) => {
  switch (lang) {
    case "EN": return "I am Ben Chan.\nHow can I help you?";
    case "JP": return "私はベンちゃんです。\n何をお手伝いできますか？";
    default:   return "Tôi là Ben Chan.\nTôi có thể giúp gì cho bạn?";
  }
};

export default function ChatBox({ lang }) {
  const [messages, setMessages] = useState([{ sender: "bot", text: getGreeting(lang) }]);
  const [lastQuestion, setLastQuestion] = useState(""); // lưu câu hỏi cuối
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [expandedResult, setExpandedResult] = useState(null);

  const chatRef = useRef(null);
  const inputRef = useRef(null);

// Khi đổi ngôn ngữ → update greeting và gọi lại API nếu có lastQuestion
  useEffect(() => {
    setMessages((prev) => {
      const newMsgs = [...prev];
      if (newMsgs.length > 0 && newMsgs[0].sender === "bot") {
        newMsgs[0] = { sender: "bot", text: getGreeting(lang) };
      }
      return newMsgs;
    });
    if (lastQuestion) {
      askIp(lastQuestion, true);
    }
  }, [lang]);

  // Auto scroll
  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
  }, [messages]);

  // Auto resize textarea
  const autoGrow = () => {
    const el = inputRef.current;
    if (!el) return;
    const cs  = getComputedStyle(el);
    const MIN = parseFloat(cs.minHeight) || 44;
    const MAX = 160;

    if (!el.value.trim()) {
      el.style.height = MIN + 'px';
      el.style.overflowY = 'hidden';
      return;
    }
    el.style.height = 'auto';
    const h = Math.min(el.scrollHeight, MAX);
    el.style.height = Math.max(h, MIN) + 'px';
    el.style.overflowY = el.scrollHeight > MAX ? 'auto' : 'hidden';
  };
  useEffect(() => { autoGrow(); }, [input]);

  // Gọi API
  const askIp = async (question, isLangSwitch = false) => {
    try {
      setLoading(true);
      setError('');
      setLastQuestion(question);

      const payload = {
        question,
        lang,
        user: { id: "u-001", email: "test@example.com", name: "Nga" }
      };

      const r = await fetch(`${import.meta.env.VITE_API_BASE}/ask-ip`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      const data = await r.json();

      const clauses = Array.isArray(data?.CLAUSES) ? data.CLAUSES.length : 0;
      const lawyers = Array.isArray(data?.LAWYERS) ? data.LAWYERS.length : 0;
      const title = `IP Chatbot — Results (${clauses} clauses · ${lawyers} lawyers)`;

      if (isLangSwitch) {
        // update kết quả cuối cùng khi đổi lang
        setMessages((m) => [
          m[0], // greeting
          { sender: 'user', text: lastQuestion },
          { sender: 'bot', type: 'result', title, data }
        ]);
      } else {
        setMessages((m) => [
          ...m,
          { sender: 'bot', type: 'result', title, data }
        ]);
      }
    } catch (e) {
      setError(String(e?.message || e));
    } finally {
      setLoading(false);
    }
  };

  const handleSend = () => {
    const q = input.trim();
    if (!q) return;
    setMessages((m) => [...m, { sender: 'user', text: q }]);
    setInput('');
    askIp(q);
  };

  return (
    <>
      <div className="chat-container">
        <div className="chat-messages" ref={chatRef}>
          {messages.map((msg, index) => (
            <div key={index} className={`msg-row ${msg.sender}`}>
              {msg.sender === 'bot' && <img className="avatar" src={botAvatar} alt="Bot" />}
              {msg.type === 'result'
                ? <ResultBubble title={msg.title} data={msg.data} lang={lang} onExpand={setExpandedResult} />
                : <div className={`message ${msg.sender}`}>{msg.text}</div>}
              {msg.sender === 'user' && <img className="avatar" src={userAvatar} alt="You" />}
            </div>
          ))}
        </div>

        <div className="input-section">
          <textarea
            ref={inputRef}
            rows={1}
            value={input}
            placeholder={
              lang === "EN" ? "Enter your question..." :
              lang === "JP" ? "質問を入力してください..." :
              "Nhập câu hỏi của bạn..."
            }
            onChange={(e) => setInput(e.target.value)}
            onInput={autoGrow}
            onKeyDown={(e) => {
              if (e.isComposing) return;
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
          />
          <button onClick={handleSend} disabled={loading}>
            {loading
              ? (lang === "EN" ? "Asking…" : lang === "JP" ? "問い合わせ中…" : "Đang hỏi…")
              : (lang === "EN" ? "Send" : lang === "JP" ? "送信" : "Gửi")}
          </button>
        </div>

        {error && <div className="card" style={{ width: '55vw', margin: '12px auto', color: 'red' }}>{error}</div>}
      </div>

      {expandedResult && <ResultOverlay result={expandedResult} onClose={() => setExpandedResult(null)} />}
    </>
  );
}
