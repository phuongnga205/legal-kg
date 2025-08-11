import { useState, useRef, useEffect } from 'react';
import './ChatBox.css';

const botAvatar = '/bot.png'; //hinh de trong thư mục public
const userAvatar = '/user.png'; //hinh de trong thư mục public

export default function ChatBox() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const chatRef = useRef(null);

  //Moi khi message thay doi, no se keo thanh cuon xuong day
  useEffect(() => {
    if(chatRef.current){
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
  },[messages]);

  const handleSend = () => {
    if (input.trim()) {
      setMessages([
        ...messages,
        { sender: 'user', text: input },
        { sender: 'bot', text: 'Tôi là Benちゃん.\nTôi có thể giúp gì cho bạn?' }
      ]);
      setInput('');
    }
  };

  return (
    <div className="chat-container">
      {/* khung tin nhắn bot */}
      <div className="chat-messages" ref={chatRef}>
        {messages.map((msg, index) => (
          <div key={index} className={`msg-row ${msg.sender}`}>
            {/* avatar vào đúng gutter */}
            {msg.sender === 'bot' && (
              <img className="avatar" src={msg.avatar || botAvatar} alt="Bot" />
            )}

            {/* bubble GIỮ NGUYÊN class .message .bot/.user */}
            <div className={`message ${msg.sender}`}>{msg.text}</div>

            {msg.sender === 'user' && (
              <img className="avatar" src={msg.avatar || userAvatar} alt="You" />
            )}
          </div>
        ))}
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