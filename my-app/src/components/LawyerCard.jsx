const toList = (s) =>
  (typeof s === "string" ? s.split(/[;,]/) : [])
    .map(x => x.trim())
    .filter(Boolean);

export default function LawyerCard({ lawyer, lang }) {
  if (!lawyer) return null;

  const name =
    (lang === "EN" && lawyer.NAME_EN) ||
    (lang === "JP" && lawyer.NAME_JP) ||
    (lang === "VN" && lawyer.NAME_VN) ||
    "";

  const specs = toList(
    (lang === "EN" && lawyer.SPECIALTY_EN) ||
    (lang === "JP" && lawyer.SPECIALTY_JP) ||
    (lang === "VN" && lawyer.SPECIALTY_VN)
  );

  const langs = toList(lawyer.LANGUAGES);

  return (
    <div className="card lawyer-card">
      <div className="card-title">{name}</div>
      <div className="card-subtitle">{lawyer.FIRM || ""}</div>
      <div className="card-row"><strong>Specialties:</strong> {specs.join(", ")}</div>
      <div className="card-row"><strong>Languages:</strong> {langs.join(", ")}</div>
      <div className="card-row"><strong>Email:</strong> {lawyer.EMAIL || "—"}</div>
      <div className="card-row"><strong>Phone:</strong> {lawyer.PHONE || "—"}</div>
    </div>
  );
}
