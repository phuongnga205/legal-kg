import ClauseCard from './ClauseCard';
import './ArticleCard.css';

export default function ArticleCard({ article, lang = "EN" }) {
  if (!article) return null;

  // Chuẩn hoá mã ngôn ngữ: EN | VI | JP
  const langMap = {
    EN: 'EN', 'EN-US': 'EN', 'EN-GB': 'EN', en: 'EN',
    VN: 'VI', VI: 'VI', vi: 'VI', 'vi-VN': 'VI',
    JP: 'JP', JA: 'JP', ja: 'JP', 'ja-JP': 'JP'
  };
  const uiLang = langMap[String(lang).toUpperCase()] || 'EN';

  // Label theo ngôn ngữ
  const LABELS = {
    ARTICLE: { EN: 'Article', VI: 'Điều', JP: 'Article' }, // muốn JP là "第{n}条" ở tiêu đề, xử lý phía dưới
    CLAUSE:  { EN: 'Clause',  VI: 'Khoản', JP: '項' },     // ✅ JP đổi thành "項"
    NO_TEXT: { EN: '(No text available)', VI: '(Chưa có nội dung)', JP: '（本文は未登録）' },
  };
  const T = (k) => LABELS[k][uiLang] || LABELS[k].EN;

  // Fallback text theo ngôn ngữ (check .trim() để tránh rỗng nhưng vẫn truthy)
  const pickText = (c) => {
    const v = (c?.text_vn ?? '').trim();
    const e = (c?.text_en ?? '').trim();
    const j = (c?.text_jp ?? '').trim();
    if (uiLang === 'VI') return v || e || j || T('NO_TEXT');
    if (uiLang === 'JP') return j || e || v || T('NO_TEXT');
    return e || v || j || T('NO_TEXT');
  };

  // Sắp xếp khoản theo số (nhẹ, không đổi cấu trúc render)
  const clauses = Array.isArray(article.clauses) ? [...article.clauses] : [];
  clauses.sort((a, b) => {
    const an = parseInt(a?.number, 10);
    const bn = parseInt(b?.number, 10);
    if (!isNaN(an) && !isNaN(bn)) return an - bn;
    return String(a?.number ?? '').localeCompare(String(b?.number ?? ''));
  });

  return (
    <div className="card article-card">
      <div className="card-title">
        {uiLang === 'JP'
          ? <>第{article.number}条 — {article.title}</>
          : <>{T('ARTICLE')} {article.number} — {article.title}</>}
      </div>

      <div className="clauses">
        {clauses.length > 0 ? (
          clauses.map((c, idx) => {
            const text = pickText(c);
            return (
              <div key={idx} className="clause-item" style={{ marginTop: 8 }}>
                <strong>
                  {uiLang === 'JP'
                    ? `第${c.number}項`
                    : `${T('CLAUSE')} ${c.number}:`}
                </strong>
                <p style={{ whiteSpace: "pre-wrap", margin: "4px 0" }}>
                  {text}
                </p>
              </div>
            );
          })
        ) : (
          <div>{T('NO_TEXT')}</div>
        )}
      </div>
    </div>
  );
}
