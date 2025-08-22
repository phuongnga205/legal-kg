import { useState } from 'react';
import ResultPanel from './ResultPanel'; //component con, sẽ render chi tiết dữ liệu kết quả (ClauseCard, LawyerCard...).

//Khai báo component ResultBubble
export default function ResultBubble({ title = 'IP Chatbot — Results', data, onExpand }) {
  return (
    <div className="message bot result-bubble">
      <button
        className="result-header"
        onClick={() => onExpand({ title, data })}  // ✅ Gọi hàm cha
        title="Xem chi tiết"
      >
        <span className="result-icon" aria-hidden>📄</span>
        <span className="result-title">{title}</span>
        <span className="result-caret" aria-hidden>⤴</span>
      </button>
    </div>
  );
}