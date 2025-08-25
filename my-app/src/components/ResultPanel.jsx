import ArticleCard from './ArticleCard';
import LawyerCard from './LawyerCard';

export default function ResultPanel({ data }) {
  if (!data) return null;

  const articles = data.ARTICLES || [];
  const lawyers = data.LAWYERS || [];

  if (articles.length === 0 && lawyers.length === 0) {
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
      {articles.length > 0 && (
        <section>
          <h3>Suggested Articles</h3>
          <div className="grid">
            {articles.map((a, idx) => (
              <ArticleCard key={idx} article={a} />
            ))}
          </div>
        </section>
      )}

      {lawyers.length > 0 && (
        <section>
          <h3>Recommended Lawyers</h3>
          <div className="grid">
            {lawyers.map((l, idx) => (
              <LawyerCard key={idx} lawyer={l} />
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
