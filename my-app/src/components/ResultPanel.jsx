import ClauseCard from './ClauseCard';
import LawyerCard from './LawyerCard';

export default function ResultPanel({ data, lang }) {   // <-- nhận thêm lang từ cha
  if (!data) return null;

  const clauses = data?.CLAUSES ?? [];
  const lawyers = data?.LAWYERS ?? [];

  const hasClauses = clauses.length > 0;
  const hasLawyers = lawyers.length > 0;

  if (!hasClauses && !hasLawyers) {
    return (
      <div className="results">
        <div className="card" style={{ marginTop: 12 }}>
          <div className="card-title">No results</div>
          <div className="card-body">Try another question.</div>
        </div>
      </div>
    );
  }

  return (
    <div className="results">
      {hasClauses && (
        <section>
          <h3>Suggested Clauses ({clauses.length})</h3>
          <div className="grid">
            {clauses.map((item, idx) => {
              const key =
                item?.CLAUSE?.CLAUSE_ID ||
                item?.ARTICLE?.ARTICLE_ID ||
                `clause-${idx}`;
              return (
                <ClauseCard key={key} item={item} lang={lang} />   
              );
            })}
          </div>
        </section>
      )}

      {hasLawyers && (
        <section style={{ marginTop: 24 }}>
          <h3>Recommended Lawyers ({lawyers.length})</h3>
          <div className="grid">
            {lawyers.map((l, idx) => (
              <LawyerCard
                key={l?.LAWYER_ID || `lawyer-${idx}`}
                lawyer={l}
                lang={lang}  
              />
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
