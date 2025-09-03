// pages/LawyerPage.jsx
import React, { useMemo, useState, useEffect } from "react";
import LawyerList from "../components/LawyerList.jsx";
import Overlay from "../components/Overlay.jsx";
import { FaSearch } from "react-icons/fa";

export default function LawyerPage({ lang = "VN", user }) {
  const [q, setQ] = useState("");
  const [lawyers, setLawyers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_BASE}/api/lawyers`)
      .then((res) => res.json())
      .then((data) => {
        console.log("Fetched lawyers:", data);

        if (!data || !data.lawyers) {
          setLawyers([]);
          setLoading(false);
          return;
        }

        const mapped = data.lawyers.map((lw, idx) => {
          if (lang === "EN") {
            return {
              id: lw.id,
              name: lw.name_en || "",
              specialty: lw.specialty_en || "",
              office: lw.firm_en || "",
              phone: lw.phone || "",
              email: lw.email || "",
              avatar: `https://i.pravatar.cc/160?img=${idx + 10}`,
              rating: 4.5,
              cases: 100,
            };
          }
          if (lang === "JP") {
            return {
              id: lw.id,
              name: lw.name_jp || "",
              specialty: lw.specialty_jp || "",
              office: lw.firm_jp || "",
              phone: lw.phone || "",
              email: lw.email || "",
              avatar: `https://i.pravatar.cc/160?img=${idx + 20}`,
              rating: 4.5,
              cases: 100,
            };
          }
          // default VN
          return {
            id: lw.id,
            name: lw.name_vn || "",
            specialty: lw.specialty_vn || "",
            office: lw.firm_vn || "",
            phone: lw.phone || "",
            email: lw.email || "",
            avatar: `https://i.pravatar.cc/160?img=${idx + 30}`,
            rating: 4.5,
            cases: 100,
          };
        });

        setLawyers(mapped);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to fetch lawyers:", err);
        setLoading(false);
      });
  }, [lang]);

  const filteredList = useMemo(() => {
    const s = q.trim().toLowerCase();
    if (!s) return lawyers;
    return lawyers.filter(
      (l) =>
        (l.name || "").toLowerCase().includes(s) ||
        (l.jpName || "").toLowerCase().includes(s) ||
        (l.specialty || "").toLowerCase().includes(s) ||
        (l.office || "").toLowerCase().includes(s)
    );
  }, [q, lawyers]);

  const text = {
    EN: {
      title: "LIST OF LAWYERS",
      placeholder: "Search by name / specialty / office…",
      total: (n) => `Total: ${n}`,
    },
    JP: {
      title: "弁護士一覧",
      placeholder: "名前・専門・勤務先で検索…",
      total: (n) => `合計: ${n}名`,
    },
    VN: {
      title: "DANH SÁCH LUẬT SƯ",
      placeholder: "Tìm theo tên / chuyên môn / nơi làm việc…",
      total: (n) => `Tổng số: ${n}`,
    },
  }[lang];

  if (loading) return <div>Loading...</div>;

  return (
    <div className="lawyer-page">
      <div className="page-header">
        <h1>{text.title}</h1>
        <div className="spacer" />
        <div className="search-wrapper">
  <input
    className="search-input"
    value={q}
    onChange={(e) => setQ(e.target.value)}
    placeholder={text.placeholder}
  />
  <FaSearch className="search-icon" />
</div>
        <div className="count">{text.total(filteredList.length)}</div>
      </div>

      <LawyerList data={filteredList} lang={lang}/>
      {!user && <Overlay lang={lang} />}
    </div>
  );
}
