import React from "react";
import "./Header.css";

const Header = () => {
  return (
    <header className="header">
      <div className="header-logo">Logo</div>
      <div className="header-info">
        <div className="header-slogan">Your Slogan Here</div>
        <div className="header-title">Tên Web</div>
      </div>
      <div className="header-right">
        <button className="header-btn">EN</button>
        <button className="header-btn">Log In</button>
      </div>
    </header>
  );
};

export default Header;