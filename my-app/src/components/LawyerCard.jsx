// components/LawyerCard.jsx
import "./LawyerCard.css";

export default function LawyerCard({ lawyer, lang }) {
  if (!lawyer) return null;

  // Kiểm tra lang hợp lệ, nếu không sẽ fallback sang 'VI'
  const currentLang = ["VI", "EN", "JP"].includes(lang) ? lang : "VI";

  const translations = {
    SPECIALTY: {
      VI: "Chuyên môn",
      EN: "Specialty",
      JP: "専門分野"
    },
    CASES: {
      VI: "Vụ án",
      EN: "Cases",
      JP: "案件数"
    },
    EMAIL: {
      VI: "Email",
      EN: "Email",
      JP: "メール"
    },
    PHONE: {
      VI: "Điện thoại",
      EN: "Phone",
      JP: "電話番号"
    },
    RATE: {
      VI: "Đánh giá",
      EN: "Rate",
      JP: "評価"
    }
  };

  return (
    <div className="lawyer-card">
      {/* Avatar */}
      <img
        src={lawyer.avatar || `https://i.pravatar.cc/160?u=${lawyer.id}`}
        alt={lawyer.name}
        className="lawyer-avatar"
      />

      {/* Tên */}
      <div className="lawyer-title">
        {lawyer.name}{" "}
      </div>

      {/* Văn phòng */}
      {lawyer.office && <div className="lawyer-subtitle">{lawyer.office}</div>}

      {/* Chuyên môn */}
      <div className="lawyer-row">
        <strong>{translations.SPECIALTY[currentLang]}:</strong>{" "}
        {lawyer.specialty || "—"}
      </div>

      {/* Rating + số vụ */}
      <div className="lawyer-row">
        <strong>{translations.RATE[currentLang]}:</strong>{" "}
        {lawyer.rating ? lawyer.rating.toFixed(2) : "—"} |{" "}
        <strong>{translations.CASES[currentLang]}:</strong>{" "}
        {lawyer.cases ?? "—"}
      </div>

      {/* Email */}
      <div className="lawyer-row">
        <strong>{translations.EMAIL[currentLang]}:</strong> {lawyer.email || "—"}
      </div>

      {/* Số điện thoại */}
      <div className="lawyer-row">
        <strong>{translations.PHONE[currentLang]}:</strong> {lawyer.phone || "—"}
      </div>
    </div>
  );
}
