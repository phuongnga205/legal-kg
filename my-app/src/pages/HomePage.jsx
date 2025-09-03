import React from "react";
import "./HomePage.css";

export default function HomePage({ lang = "VN" }) {
  const text = {
    EN: {
      heading: <>Welcome to <span className="highlight">Benvise</span></>,
      description: `<span class="highlight">Benvise</span> – where <span class="highlight">Ben-chan</span>, your intelligent companion, is always ready to provide helpful legal advice on Intellectual Property. From trademarks and copyrights to patents, <span class="highlight">Ben-chan</span> helps you understand the law more clearly so you can live with peace of mind.`,
    },
    JP: {
      heading: <>ようこそ <span className="highlight">Benvise</span>へ</>,
      description: `<span class="highlight">Benvise</span>では、あなたの賢いパートナーである <span class="highlight">ベンちゃん</span> が、知的財産に関する役立つ法的アドバイスをいつでもお届けします。商標、著作権、特許まで、<span class="highlight">ベンちゃん</span> は法律をわかりやすく解説し、安心して生活できるようサポートします。`,
    },
    VN: {
      heading: <>Chào mừng đến với <span className="highlight">Benvise</span></>,
      description: `<span class="highlight">Benvise</span> – nơi <span class="highlight">Ben-chan</span>, người bạn đồng hành thông minh, luôn sẵn sàng mang đến những lời khuyên pháp lý hữu ích về Sở hữu trí tuệ. Từ nhãn hiệu, bản quyền đến sáng chế, <span class="highlight">Ben-chan</span> giúp bạn hiểu luật rõ ràng hơn để sống an tâm hơn.`,
    },
  }[lang];

  return (
    <div className="home-container">
      <div className="home-image">
        <img src="ben-chan.png" alt="Home" />
      </div>
      <div className="home-content">
        <h1>{text.heading}</h1>
        {/* Render description có HTML highlight */}
        <p dangerouslySetInnerHTML={{ __html: text.description }} />
      </div>
    </div>
  );
}
