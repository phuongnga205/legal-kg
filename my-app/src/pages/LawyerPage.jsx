// pages/LawyerPage.jsx
import React, { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import LawyerList from "../components/LawyerList.jsx";
import Overlay from "../components/Overlay.jsx";


// Mock data
const MOCK_LAWYERS = [
  {
    id: "lw_001",
    name: "Nguyễn Minh Anh",
    jpName: "グエン・ミン・アン",
    specialty: "Trademark • Opposition • Appeal",
    cases: 128,
    office: "Hanoi, VN",
    rating: 4.8,
    avatar: "https://i.pravatar.cc/160?img=32",
  },
  {
    id: "lw_002",
    name: "Trần Hải Long",
    jpName: "チャン・ハイ・ロン",
    specialty: "Patent • Invalidation • Licensing",
    cases: 203,
    office: "Ho Chi Minh City, VN",
    rating: 4.9,
    avatar: "https://i.pravatar.cc/160?img=12",
  },
  {
    id: "lw_003",
    name: "Lê Thu Phương",
    jpName: "レ・トゥ・フオン",
    specialty: "Copyright • Enforcement • Negotiation",
    cases: 95,
    office: "Da Nang, VN",
    rating: 4.7,
    avatar: "https://i.pravatar.cc/160?img=56",
  },
  {
    id: "lw_004",
    name: "Phạm Quang Dũng",
    jpName: "ファム・クアン・ズン",
    specialty: "Design • Prosecution • Litigation",
    cases: 141,
    office: "HCMC • VN",
    rating: 4.85,
    avatar: "https://i.pravatar.cc/160?img=5",
  },
];


export default function LawyerPage({ lang = "VN", user }) {
  const [q, setQ] = useState("");

  const filteredList = useMemo(() => {
    const s = q.trim().toLowerCase();
    if (!s) return MOCK_LAWYERS;
    return MOCK_LAWYERS.filter(
      (l) =>
        l.name.toLowerCase().includes(s) ||
        l.jpName.toLowerCase().includes(s) ||
        l.specialty.toLowerCase().includes(s) ||
        l.office.toLowerCase().includes(s)
    );
  }, [q]);

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

  return (
    <div className="lawyer-page">
      <div className="page-header">
        <h1>{text.title}</h1>
        <div className="spacer" />
        <input
          className="search-input"
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder={text.placeholder}
        />
        <div className="count">{text.total(filteredList.length)}</div>
      </div>

      <LawyerList data={filteredList} />
      {!user && <Overlay lang={lang} />}
    </div>
  );
}
