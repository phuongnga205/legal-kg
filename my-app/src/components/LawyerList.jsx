// components/LawyerList.jsx
import { motion } from "framer-motion";
import "./LawyerList.css";

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.12, delayChildren: 0.05 },
  },
};

const item = {
  hidden: { opacity: 0, y: 16 },
  show: { opacity: 1, y: 0, transition: { type: "spring", stiffness: 140, damping: 18 } },
};

// 🔤 Label đa ngôn ngữ
const LABELS = {
  SPECIALTY: { EN: "Specialty", VI: "Chuyên môn", JP: "専門分野" },
  CASES: { EN: "Cases", VI: "Vụ án", JP: "案件" },
  OFFICE: { EN: "Law Firm", VI: "Văn phòng luật", JP: "法律事務所" },
  CONTACT: { EN: "Contact", VI: "Liên hệ", JP: "連絡する" },
  DETAIL: { EN: "View details", VI: "Xem chi tiết", JP: "詳細を見る" },
  BIO: {
    EN: "Experienced IP attorney for Vietnam–Japan cross-border filings and disputes.",
    VI: "Luật sư SHTT giàu kinh nghiệm về hồ sơ và tranh chấp xuyên biên giới Việt–Nhật.",
    JP: "ベトナムと日本の越境出願や紛争に豊富な経験を持つ知財弁護士です。",
  },
};

// Chuẩn hóa lang
function normalizeLang(lang) {
  const map = {
    EN: "EN", "EN-US": "EN", "EN-GB": "EN", en: "EN",
    VI: "VI", VN: "VI", vi: "VI", "vi-VN": "VI",
    JP: "JP", JA: "JP", ja: "JP", "ja-JP": "JP",
  };
  return map[String(lang).toUpperCase()] || "EN";
}

function Card({ lawyer, lang = "EN" }) {
  const uiLang = normalizeLang(lang);

  return (
    <div className="lw-card">
      <img className="lw-avatar" src={lawyer.avatar} alt={lawyer.name} loading="lazy" />
      <div className="lw-body">
        <div className="lw-row">
          <h3 className="lw-name">{lawyer.name}</h3>
          <div className="lw-rating" title={`Rating ${lawyer.rating}`}>
            {"★★★★★☆☆☆☆☆".slice(5 - Math.round(lawyer.rating), 10 - Math.round(lawyer.rating))}
            <span className="lw-rating-num">{lawyer.rating.toFixed(2)}</span>
          </div>
        </div>

        <div className="lw-chips">
          <span className="lw-chip">
            {LABELS.SPECIALTY[uiLang]}: {lawyer.specialty}
          </span>
          <span className="lw-chip">
            {LABELS.CASES[uiLang]}: {lawyer.cases}
          </span>
          <span className="lw-chip">
            {LABELS.OFFICE[uiLang]}: {lawyer.office}
          </span>
        </div>

        <p className="lw-bio">{LABELS.BIO[uiLang]}</p>

        <div className="lw-actions">
          <button className="lw-btn-primary">{LABELS.CONTACT[uiLang]}</button>
          <button className="lw-btn-ghost">{LABELS.DETAIL[uiLang]}</button>
        </div>
      </div>
    </div>
  );
}

function LawyerList({ data, lang = "EN" }) {
  const uiLang = normalizeLang(lang);

  return (
    <motion.div
      className="lw-grid"
      variants={container}
      initial="hidden"
      animate="show"
      layout
    >
      {data.map((lw) => (
        <motion.div key={lw.id} variants={item}>
          <Card lawyer={lw} lang={uiLang} />
        </motion.div>
      ))}
    </motion.div>
  );
}

export default LawyerList;
