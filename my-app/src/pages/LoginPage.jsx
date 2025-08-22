import React, { useState } from "react";

export default function LoginPage({ lang, setUser }) {
  const [form, setForm] = useState({ email: "", password: "" });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // 🟢 Login giả lập: chỉ cần set user
    setUser({ name: "User Demo", email: form.email });
  };

  // Text theo ngôn ngữ
  const text = {
    EN: { title: "Log In", email: "Email", password: "Password", submit: "Log In" },
    JP: { title: "ログイン", email: "メール", password: "パスワード", submit: "ログイン" },
    VN: { title: "Đăng nhập", email: "Email", password: "Mật khẩu", submit: "Đăng nhập" },
  }[lang];

  return (
    <div className="auth-page">
      <h2>{text.title}</h2>
      <form onSubmit={handleSubmit} className="auth-form">
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
