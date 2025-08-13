import React from "react";
import "./HomePage.css";

export default function HomePage() {
  return (
    <div className="home-container">
      <div className="home-image">
        <img src="Tanjiro_Kamado.png" alt="Home" />
      </div>
      <div className="home-content">
        <h1>ようこそベンちゃんへ</h1>
        <p>
          Đây là nội dung mô tả ngắn gọn. Bạn có thể thay thế bằng đoạn giới thiệu
          hoặc thông tin bất kỳ.
        </p>
      </div>
    </div>
  );
}