export default function LawyerCard({ lawyer, lang = "EN" }) {
  if (!lawyer) return null;

  // chọn đúng ngôn ngữ
  const name =
    (lang === "EN" && lawyer.name_en) ||
    (lang === "JP" && lawyer.name_jp) ||
    (lang === "VN" && lawyer.name_vn) ||
    "";

  const firm =
    (lang === "EN" && lawyer.firm_en) ||
    (lang === "JP" && lawyer.firm_jp) ||
    (lang === "VN" && lawyer.firm_vn) ||
    "";

  const specialty =
    (lang === "EN" && lawyer.specialty_en) ||
    (lang === "JP" && lawyer.specialty_jp) ||
    (lang === "VN" && lawyer.specialty_vn) ||
    "";

  // labels theo ngôn ngữ
  const labels = {
    EN: { specialty: "Specialty", email: "Email", phone: "Phone" },
    JP: { specialty: "専門", email: "メール", phone: "電話" },
    VN: { specialty: "Chuyên môn", email: "Email", phone: "Điện thoại" },
  };
  const t = labels[lang] || labels.EN;

  return (
    <div className="card lawyer-card">
      <div className="card-title">{name}</div>
      {firm && <div className="card-subtitle">{firm}</div>}
      <div className="card-row">
        <strong>{t.specialty}:</strong> {specialty || "—"}
      </div>
      <div className="card-row">
        <strong>{t.email}:</strong> {lawyer.email || "—"}
      </div>
      <div className="card-row">
        <strong>{t.phone}:</strong> {lawyer.phone || "—"}
      </div>
    </div>
  );
}
