export default function ClauseCard({ item, lang }) {
  if (!item) return null;

  const LAW = item.LAW || {};
  const ARTICLE = item.ARTICLE || {};
  const CLAUSE = item.CLAUSE || {};

  // chọn đúng field theo lang
  const lawName =
    (lang === "EN" && LAW.NAME_EN) ||
    (lang === "JP" && LAW.NAME_JP) ||
    (lang === "VN" && LAW.NAME_VN) ||
    ""; 

  const title =
    (lang === "EN" && ARTICLE.TITLE_EN) ||
    (lang === "JP" && ARTICLE.TITLE_JP) ||
    (lang === "VN" && ARTICLE.TITLE_VN) ||
    "";

  const text =
    (lang === "EN" && CLAUSE.TEXT_EN) ||
    (lang === "JP" && CLAUSE.TEXT_JP) ||
    (lang === "VN" && CLAUSE.TEXT_VN) ||
    "";

  return (
    <div className="card clause-card">
      <div className="card-title">
        Article {ARTICLE.NUMBER ?? ""} — Clause {CLAUSE.NUMBER ?? ""}
      </div>
      <div className="card-subtitle">{lawName}</div>
      {title && <div className="mt-1 font-medium">{title}</div>}
      <p className="card-body" style={{ whiteSpace: "pre-wrap" }}>{text}</p>
      {LAW.LINK && (
        <a className="card-link" href={LAW.LINK} target="_blank" rel="noreferrer">
          View source
        </a>
      )}
    </div>
  );
}
