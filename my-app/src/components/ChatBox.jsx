import { useState, useRef, useEffect } from 'react';
import './ChatBox.css';

const botAvatar = '/bot.png'; //hinh de trong thư mục public
const userAvatar = '/user.png'; //hinh de trong thư mục public

export default function ChatBox() {
  const [messages, setMessages] = useState([
     { sender: 'bot', text: 'Tôi là Benちゃん.\nTôi có thể giúp gì cho bạn?' }
  ]);
  const [input, setInput] = useState('');
  const chatRef = useRef(null);
   // thêm ref cho textarea
  const inputRef = useRef(null);

   // hàm autoGrow
  const autoGrow = () => {
    const el = inputRef.current;
    if (!el) return;

    const cs  = getComputedStyle(el);
    const MIN = parseFloat(cs.minHeight) || 44; // bằng nút
    const MAX = 160;

    // Khi rỗng: luôn đúng bằng MIN (bằng nút)
    if (!el.value.trim()) {
      el.style.height = MIN + 'px';
      el.style.overflowY = 'hidden';
      return;
    }

    // Có nội dung: nở dần tới MAX rồi mới cuộn
    el.style.height = 'auto';
    const h = Math.min(el.scrollHeight, MAX);
    el.style.height = Math.max(h, MIN) + 'px';
    el.style.overflowY = el.scrollHeight > MAX ? 'auto' : 'hidden';
  };
  //Moi khi message thay doi, no se keo thanh cuon xuong day
  useEffect(() => {
    if(chatRef.current){
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
  },[messages]);

  // auto-resize lại khi nội dung input đổi
  useEffect(() => {
    autoGrow();
  }, [input]);

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
        <textarea
          ref={inputRef}
          rows={1}
          value={input}
          placeholder="Nhập câu hỏi của bạn..."
          onChange={(e) => setInput(e.target.value)}
          onInput={autoGrow}
          onKeyDown={(e) => {
            if (e.isComposing) return;
            //Enter = gửi, Shift+Enter = xuống dòng
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              handleSend();
            }
          }}
        />
        <button onClick={handleSend}>Gửi</button>
      </div>
    </div>
  );
}