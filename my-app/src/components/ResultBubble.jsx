export default function ResultBubble({ data, onExpand }) {
  if (!data) return null;

  // 🔑 Đúng key: ARTICLES và LAWYERS
  const totalClauses = (data.ARTICLES || []).reduce(
    (sum, a) => sum + (a.clauses?.length || 0),
    0
  );
  const totalLawyers = (data.LAWYERS || []).length;

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
