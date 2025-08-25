import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function RegisterPage({ lang }) {
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const res = await fetch("http://127.0.0.1:8000/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });

      const data = await res.json();

      if (res.ok) {
        alert("Register success! Please login.");
        navigate("/login"); // ✅ chuyển qua trang login
      } else {
        setError(data.msg || "Register failed");
      }
    } catch (err) {
      setError("Server error");
    }
  };

  const text = {
    EN: { title: "Sign Up", name: "Name", email: "Email", password: "Password", submit: "Sign Up" },
    JP: { title: "サインアップ", name: "名前", email: "メール", password: "パスワード", submit: "登録" },
    VN: { title: "Đăng ký", name: "Tên", email: "Email", password: "Mật khẩu", submit: "Đăng ký" },
  }[lang];

  return (
    <div className="auth-page">
      <h2>{text.title}</h2>
      <form onSubmit={handleSubmit} className="auth-form">
        <input type="text" name="name" placeholder={text.name} value={form.name} onChange={handleChange} required />
        <input type="email" name="email" placeholder={text.email} value={form.email} onChange={handleChange} required />
        <input type="password" name="password" placeholder={text.password} value={form.password} onChange={handleChange} required />
        <button type="submit">{text.submit}</button>
      </form>
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}
