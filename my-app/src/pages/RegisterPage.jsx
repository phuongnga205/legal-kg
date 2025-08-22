import React, { useState } from "react";

export default function RegisterPage({ lang, setUser }) {
  const [form, setForm] = useState({ name: "", email: "", password: "" });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // 🟢 Register giả lập: tạo user mới
    setUser({ name: form.name, email: form.email });
  };

  // Text theo ngôn ngữ
  const text = {
    EN: { title: "Sign Up", name: "Name", email: "Email", password: "Password", submit: "Sign Up" },
    JP: { title: "サインアップ", name: "名前", email: "メール", password: "パスワード", submit: "登録" },
    VN: { title: "Đăng ký", name: "Tên", email: "Email", password: "Mật khẩu", submit: "Đăng ký" },
  }[lang];

  return (
    <div className="auth-page">
      <h2>{text.title}</h2>
      <form onSubmit={handleSubmit} className="auth-form">
        <input
          type="text"
          name="name"
          placeholder={text.name}
          value={form.name}
          onChange={handleChange}
          required
        />
        <input
          type="email"
          name="email"
          placeholder={text.email}
          value={form.email}
          onChange={handleChange}
          required
        />
        <input
          type="password"
          name="password"
          placeholder={text.password}
          value={form.password}
          onChange={handleChange}
          required
        />
        <button type="submit">{text.submit}</button>
      </form>
    </div>
  );
}
