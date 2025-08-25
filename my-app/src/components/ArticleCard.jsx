import ClauseCard from './ClauseCard';

export default function ArticleCard({ article, lang = "EN" }) {
  if (!article) return null;

  return (
    <div className="card article-card">
      <div className="card-title">
        Article {article.number} — {article.title}
      </div>

      <div className="clauses">
        {Array.isArray(article.clauses) && article.clauses.length > 0 ? (
          article.clauses.map((c, idx) => {
            // chọn text theo ngôn ngữ
            const text =
              (lang === "VN" && c.text_vn) ||
              (lang === "JP" && c.text_jp) ||
              c.text_en ||
              "(No text available)";

            return (
              <div key={idx} className="clause-item" style={{ marginTop: 8 }}>
                <strong>Clause {c.number}:</strong>
                <p style={{ whiteSpace: "pre-wrap", margin: "4px 0" }}>
                  {text}
                </p>
              </div>
            );
          })
        ) : (
          <div>No clauses</div>
        )}
      </div>
    </div>
  );
}
