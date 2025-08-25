import { useState } from 'react';
import ResultPanel from './ResultPanel';

export default function ResultBubble({ data, onExpand }) {
  if (!data) return null;

  // Tính tổng clause trong tất cả articles
  const totalClauses = (data.articles || []).reduce(
    (sum, a) => sum + (a.clauses?.length || 0),
    0
  );
  const totalLawyers = (data.lawyers || []).length;

  // Tiêu đề động
  const title = `IP Chatbot — Results (${totalClauses} clauses · ${totalLawyers} lawyers)`;

  return (
    <div className="message bot result-bubble">
      <button
        className="result-header"
        onClick={() => onExpand({ title, data })}
        title="Xem chi tiết"
      >
        <span className="result-icon" aria-hidden>📄</span>
        <span className="result-title">{title}</span>
        <span className="result-caret" aria-hidden>⤴</span>
      </button>
    </div>
  );
}
