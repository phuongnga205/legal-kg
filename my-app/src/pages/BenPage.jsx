import React from 'react';
import { Link } from 'react-router-dom';
import ChatBox from '../components/ChatBox';
import './BenPage.css';

const BenPage = ({ lang, user }) => {
  return (
    <div className="benchan-page">
      <ChatBox lang={lang} />

      {!user && (
        <div className="overlay">
          <div className="overlay-content">
            <h2>
              {lang === "EN"
                ? "You need to log in or sign up to use this feature"
                : lang === "JP"
                ? "この機能を利用するにはログインまたは登録が必要です"
                : "Bạn cần đăng nhập hoặc đăng ký để sử dụng"}
            </h2>
            <div className="overlay-buttons">
              <Link to="/login" className="overlay-btn">
                {lang === "EN" ? "Log In" : lang === "JP" ? "ログイン" : "Đăng nhập"}
              </Link>
              <Link to="/register" className="overlay-btn">
                {lang === "EN" ? "Sign Up" : lang === "JP" ? "登録" : "Đăng ký"}
              </Link>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default BenPage;
