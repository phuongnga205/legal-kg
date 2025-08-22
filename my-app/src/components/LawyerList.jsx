// components/LawyerList.jsx
import { memo } from "react";
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

function Card({ lawyer }) {
  return (
    <div className="lw-card">
      <img className="lw-avatar" src={lawyer.avatar} alt={lawyer.name} loading="lazy" />
      <div className="lw-body">
        <div className="lw-row">
          <h3 className="lw-name">
            {lawyer.name} <span className="lw-jp">{lawyer.jpName}</span>
          </h3>
          <div className="lw-rating" title={`Rating ${lawyer.rating}`}>
            {"★★★★★☆☆☆☆☆".slice(5 - Math.round(lawyer.rating), 10 - Math.round(lawyer.rating))}
            <span className="lw-rating-num">{lawyer.rating.toFixed(2)}</span>
          </div>
        </div>

        <div className="lw-chips">
          <span className="lw-chip">{lawyer.specialty}</span>
          <span className="lw-chip">案件: {lawyer.cases}</span>
          <span className="lw-chip">{lawyer.office}</span>
        </div>

        <p className="lw-bio">
          Experienced IP attorney for Vietnam–Japan cross‑border filings and disputes.
        </p>

        <div className="lw-actions">
          <button className="lw-btn-primary">Liên hệ</button>
          <button className="lw-btn-ghost">Xem chi tiết</button>
        </div>
      </div>
    </div>
  );
}

function LawyerList({ data }) {
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
          <Card lawyer={lw} />
        </motion.div>
      ))}
    </motion.div>
  );
}

export default LawyerList;
