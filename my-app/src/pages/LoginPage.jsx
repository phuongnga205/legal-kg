import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { FaUser, FaLock, FaEnvelope } from "react-icons/fa";
import "./User.css";

export default function LoginPage({ lang, setUser }) {
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const res = await fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });

      const data = await res.json();

      if (res.ok) {
        setUser(data.user); // ✅ App.jsx sẽ tự lưu vào localStorage
        navigate("/"); // ✅ sau khi login thành công → về trang Home
      } else {
        setError(data.msg || "Login failed");
      }
    } catch (err) {
      setError("Server error");
    }
  };

  const text = {
    EN: { title: "LOGIN", email: "Email", password: "Password", submit: "LOGIN" },
    JP: { title: "ログイン", email: "メール", password: "パスワード", submit: "ログイン" },
    VN: { title: "ĐĂNG NHẬP", email: "Email", password: "Mật khẩu", submit: "Đăng nhập" },
  }[lang];

  return (
    <div className="auth-page">
      <h2>{text.title}</h2>
      <form onSubmit={handleSubmit} className="auth-form">
        {/* 📧 input email */}
        <div className="input-group">
          <FaEnvelope className="icon" />
          <input
            type="email"
            name="email"
            placeholder={text.email}
            value={form.email}
            onChange={handleChange}
            required
          />
        </div>

        {/* 🔑 input mật khẩu */}
        <div className="input-group">
          <FaLock className="icon" />
          <input
            type="password"
            name="password"
            placeholder={text.password}
            value={form.password}
            onChange={handleChange}
            required
          />
        </div>
        <button type="submit">{text.submit}</button>
      </form>
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}
