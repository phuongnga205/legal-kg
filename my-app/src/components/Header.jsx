import React from "react";
import "./Header.css";
import { useNavigate } from "react-router-dom";


const Header = ({ lang, setLang }) => {
  const navigate = useNavigate();
  const handleLangChange = (newLang) => {
    setLang(newLang);
    console.log("Language changed:", newLang);
  };

  return (
    <header className="header">
      <div className="header-logo">Logo</div>

      <div className="header-info">
        <div className="header-slogan">
          {lang === "EN" ? "Your Slogan Here" :
          lang === "JP" ? "あなたのスローガン" :
          "Khẩu hiệu của bạn"}
        </div>
        
        <div className="header-title">
          {lang === "EN" ? "Website Name" :
          lang === "JP" ? "ウェブサイト名" :
          "Tên Web"}
        </div>
      </div>

      {/* Gom login/register và language vào 1 hàng */}
      <div className="auth-lang-group">
        <div className="auth-buttons">
          <button 
            className="header-btn"
            onClick={() => navigate("/login")}  //  thêm điều hướng
          >
            {lang === "EN" ? "Log In" :
            lang === "JP" ? "ログイン" :
            "Đăng nhập"}
          </button>
          <button 
            className="header-btn"
            onClick={() => navigate("/register")} // thêm điều hướng
          >
            {lang === "EN" ? "Sign Up" :
            lang === "JP" ? "サインアップ" :
            "Đăng ký"}
          </button>
        </div>

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
