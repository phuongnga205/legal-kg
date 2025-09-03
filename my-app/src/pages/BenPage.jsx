import React, { useState } from 'react';
import ChatBox from '../components/ChatBox';
import ChatHistory from '../components/ChatHistory';
import Overlay from "../components/Overlay.jsx";

const BenPage = ({ lang, user }) => {
  const [history, setHistory] = useState([]);
  const [selectedQ, setSelectedQ] = useState(null);
  const [resetKey, setResetKey] = useState(0); // key để reset ChatBox
  const [sessionId, setSessionId] = useState("sess-" + Date.now()); // 🆕 sessionId mặc định

  // Hàm tạo Chat mới
  const handleNewChat = () => {
    const newId = "sess-" + Date.now();  // tạo sessionId mới theo timestamp
    setSessionId(newId);
    setSelectedQ(null);
    setResetKey(prev => prev + 1); // tăng key => ChatBox remount
  };

  return (
    <div className="benchan-page">
      <div className="benchan-layout">
        <ChatHistory 
          history={history} 
          onSelect={setSelectedQ} 
          onNewChat={handleNewChat}
          lang={lang} 
        />

        <ChatBox 
          key={resetKey}          // đổi key => reset ChatBox state
          lang={lang}
          sessionId={sessionId}   // 🆕 truyền sessionId xuống ChatBox
          selectedQ={selectedQ}
          onNewQuestion={(q) => setHistory((h) => [...h, q])}
        />
      </div>

      {!user && <Overlay lang={lang} />}
    </div>
  );
};

export default BenPage;
