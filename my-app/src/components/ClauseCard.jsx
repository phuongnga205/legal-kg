export default function ClauseCard({ clause }) {
  if (!clause) return null;

  return (
    <div className="clause-card">
      <div className="clause-number">Clause {clause.number ?? "?"}</div>
      <p className="clause-text" style={{ whiteSpace: "pre-wrap" }}>
        {clause.text}
      </p>
    </div>
  );
}
