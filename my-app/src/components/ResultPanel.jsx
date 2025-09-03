import ArticleCard from './ArticleCard';
import LawyerCard from './LawyerCard';
import './ResultPanel.css';

export default function ResultPanel({ data, lang }) {
  if (!data) return null;

  // 🔑 đọc đúng keys từ backend mới
  const articles = data.ARTICLES || [];
  const lawyers  = data.LAWYERS  || [];

  // Nếu parent không truyền lang riêng thì lấy từ response
  const rawLang = (lang || data.lang || 'EN');

  // Chuẩn hoá mã ngôn ngữ → EN | VI | JP
  const langMap = {
    EN: 'EN', 'en': 'EN', 'en-US': 'EN', 'en-GB': 'EN',
    VI: 'VI', 'VN': 'VI', 'vi': 'VI', 'vi-VN': 'VI',
    JP: 'JP', 'JA': 'JP', 'ja': 'JP', 'ja-JP': 'JP'
  };
  const uiLang = langMap[String(rawLang).toUpperCase()] || 'EN';

  const translations = {
    NO_RESULTS: {
      EN: "No results",
      VI: "Không có kết quả",
      JP: "結果がありません"
    },
    TRY_ANOTHER: {
      EN: "Try another question.",
      VI: "Hãy thử câu hỏi khác.",
      JP: "別の質問を試してください。"
    },
    SUGGESTED_ARTICLES: {
      EN: "Suggested Clauses",    
      VI: "Điều khoản đề xuất",    
      JP: "おすすめの条項"  
    },
    RECOMMENDED_LAWYERS: {
      EN: "Recommended Lawyers",
      VI: "Luật sư đề xuất",
      JP: "おすすめの弁護士"
    }
  };

  // Helper lấy text theo ngôn ngữ, có fallback EN
  const T = (key) =>
    (translations[key] && (translations[key][uiLang] || translations[key].EN)) || '';

  if (articles.length === 0 && lawyers.length === 0) {
    return (
      <div className="results">
        <div className="card" style={{ marginTop: 12 }}>
          <div className="card-title">{T('NO_RESULTS')}</div>
          <div className="card-body">{T('TRY_ANOTHER')}</div>
        </div>
      </div>
    );
  }

  return (
    <div className="results">
      {(articles.length > 0 || lawyers.length > 0) && (
        <div className="result-columns">
          {articles.length > 0 && (
            <section className="left-column">
              <h3>{T('SUGGESTED_ARTICLES')}</h3>
              <div className="grid">
                {articles.map((a, idx) => (
                  <ArticleCard key={idx} article={a} lang={uiLang} />
                ))}
              </div>
            </section>
          )}

          {lawyers.length > 0 && (
            <section className="right-column">
              <h3>{T('RECOMMENDED_LAWYERS')}</h3>
              <div className="grid">
                {lawyers.map((l, idx) => (
                  <LawyerCard key={idx} lawyer={l} lang={uiLang} />
                ))}
              </div>
            </section>
          )}
        </div>
      )}
    </div>
  );
}
