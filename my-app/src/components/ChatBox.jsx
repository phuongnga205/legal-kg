import { useState } from 'react';
import './ChatBox.css';

export default function ChatBox() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (input.trim()) {
      setMessages([
        ...messages,
        { sender: 'user', text: input },
        { sender: 'bot', text: 'Tôi là Benちゃん. Tôi có thể giúp gì cho bạn?' }
      ]);
      setInput('');
    }
  };

  return (
    <div className="chat-container">
      {/* logo hình tròn chữ 弁 */}
      <div className="chat-logo">弁</div>

      {/* khung tin nhắn bot */}
      <div className="chat-messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            {msg.text}
          </div>
        ))}
      </div>

      {/* cột phải: avatar + tin nhắn người dùng */}
      <div className="chat-right">
        <div className="user-message-preview">
          {messages.length > 0 && messages[messages.length - 2]?.sender === 'user'
            ? messages[messages.length - 2].text
            : ''}
        </div>
        <div className="user-avatar"></div>
      </div>

      {/* ô nhập + nút gửi */}
      <div className="input-section">
        <input
          type="text"
          value={input}
          placeholder="Nhập câu hỏi của bạn..."
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
        />
        <button onClick={handleSend}>Gửi</button>
      </div>
    </div>
  );
}