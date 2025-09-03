import React from "react";
import "./Header.css";
import { useNavigate } from "react-router-dom";

const Header = ({ lang, setLang, user, setUser, onLogout }) => {
  const navigate = useNavigate();

  const handleLangChange = (newLang) => {
    setLang(newLang);
    console.log("Language changed:", newLang);
  };

  return (
    <header className="header">
      <div className="header-logo">
        <img src="/logo.png" alt="Logo" style={{ height: "40px" }} />
      </div>

      <div className="header-info">
        <div className="header-slogan">
          {lang === "EN"
            ? "Know Law – Live Safe"
            : lang === "JP"
            ? "法律を知り、安全に生きる"
            : "Hiểu luật – Sống an"}
        </div>

        <div className="header-title">
          BENVISE
        </div>
      </div>

      <div className="auth-lang-group">
        {user ? (
          <div
            className="auth-buttons"
            style={{ display: "flex", alignItems: "center", gap: "8px" }}
          >
            <img
              src="/user.png"
              alt="User"
              style={{
                width: "28px",
                height: "28px",
                borderRadius: "50%",
                objectFit: "cover",
              }}
            />
            <span>{user.name}</span>
            <button
              className="header-btn"
              onClick={() => {
                onLogout();
                navigate("/");
              }}
            >
              {lang === "EN" ? "Logout" : lang === "JP" ? "ログアウト" : "Đăng xuất"}
            </button>
          </div>
        ) : (
          <div className="auth-buttons">
            <button className="header-btn" onClick={() => navigate("/login")}>
              {lang === "EN" ? "Log In" : lang === "JP" ? "ログイン" : "Đăng nhập"}
            </button>
            <button className="header-btn" onClick={() => navigate("/register")}>
              {lang === "EN" ? "Sign Up" : lang === "JP" ? "サインアップ" : "Đăng ký"}
            </button>
          </div>
        )}

        <div className="lang-switcher">
          <button
            className={`lang-btn ${lang === "EN" ? "active" : ""}`}
            onClick={() => handleLangChange("EN")}
          >
            EN
          </button>
          <button
            className={`lang-btn ${lang === "JP" ? "active" : ""}`}
            onClick={() => handleLangChange("JP")}
          >
            JP
          </button>
          <button
            className={`lang-btn ${lang === "VN" ? "active" : ""}`}
            onClick={() => handleLangChange("VN")}
          >
            VN
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;
