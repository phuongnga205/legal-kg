import React from "react";
import "./HomePage.css";

export default function HomePage({ lang = "VN" }) {
  const text = {
    EN: {
      heading: "Welcome to Ben-chan",
      description: "This is a short introduction. You can replace it with any message or information.",
    },
    JP: {
      heading: "ようこそベンちゃんへ",
      description: "これは短い紹介文です。任意のメッセージや情報に置き換えることができます。",
    },
    VN: {
      heading: "Chào mừng đến với Bên-chan",
      description: "Đây là nội dung mô tả ngắn gọn. Bạn có thể thay thế bằng đoạn giới thiệu hoặc thông tin bất kỳ.",
    },
  }[lang];

  return (
    <div className="home-container">
      <div className="home-image">
        <img src="Tanjiro_Kamado.png" alt="Home" />
      </div>
      <div className="home-content">
        <h1>{text.heading}</h1>
        <p>{text.description}</p>
      </div>
    </div>
  );
}
