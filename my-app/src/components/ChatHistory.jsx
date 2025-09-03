import React, { useState } from "react";
import { ChevronDownIcon, ChevronUpIcon } from "@heroicons/react/24/solid"; // ✅ import Heroicons
import "./ChatHistory.css";

export default function ChatHistory({ history, onSelect, onNewChat, lang }) {
  const [showHistory, setShowHistory] = useState(true);

  const translations = {
    NEW: { EN: "New Chat", VN: "Chat mới", JP: "新しいチャット" },
    HISTORY: { EN: "Chat history", VN: "Lịch sử hội thoại", JP: "チャット履歴" },
    EMPTY: { EN: "No conversations yet", VN: "Chưa có hội thoại nào", JP: "会話はまだありません" },
  };

  return (
    <div className="chat-history-container">
      {/* Tab Chat mới */}
      <div className="history-header new-chat-item" onClick={onNewChat}>
        {translations.NEW[lang] || translations.NEW.VN}
      </div>

      {/* Toggle lịch sử hội thoại */}
      <div
        className="history-header history-toggle"
        onClick={() => setShowHistory(!showHistory)}
      >
        <span>{translations.HISTORY[lang] || translations.HISTORY.VN}</span>
        {showHistory ? (
          <ChevronUpIcon className="h-5 w-5 arrow" />
        ) : (
          <ChevronDownIcon className="h-5 w-5 arrow" />
        )}
      </div>

      {/* Danh sách hội thoại */}
      {showHistory && (
        <ul className="history-list">
          {history.length === 0 ? (
            <li className="empty">
              {translations.EMPTY[lang] || translations.EMPTY.VN}
            </li>
          ) : (
            history.map((q, i) => (
              <li key={i} onClick={() => onSelect(q)}>
                <span>{q}</span>
              </li>
            ))
          )}
        </ul>
      )}
    </div>
  );
}
