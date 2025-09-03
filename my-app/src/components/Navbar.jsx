import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

const Navbar = ({ lang }) => {
  // dictionary đa ngôn ngữ
  const labels = {
    EN: { home: "Home", ben: "Ben Chan", lawyer: "Lawyer" },
    JP: { home: "ホーム", ben: "ベンちゃん", lawyer: "弁護士" },
    VN: { home: "Trang chủ", ben: "Ben Chan", lawyer: "Luật sư" },
  };

  const t = labels[lang] || labels.EN; // fallback = EN

  return (
    <nav className="navbar">
      <ul>
        <li><Link to="/">{t.home}</Link></li>
        <li><Link to="/benchan">{t.ben}</Link></li>
        <li><Link to="/lawyer">{t.lawyer}</Link></li>
      </ul>
    </nav>
  );
};

export default Navbar;

