import React, { useEffect, useState } from 'react';   
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Navbar from './components/Navbar';
import HomePage from './pages/HomePage';
import BenPage from './pages/BenPage';
import LawyerPage from './pages/LawyerPage'; 
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import './App.css';

function App() {
  const [lang, setLang] = useState("EN"); //thêm state cho ngôn ngữ
  const [user, setUser] = useState(null);  // 🟢 thêm user state

  //Tính khoảng đệm dưới header + navbar
  useEffect(() => {
    const setTopOffset = () => {
      const h = document.querySelector('.header');
      const n = document.querySelector('.navbar');
      const hH = h ? h.offsetHeight : 0;
      const nH = n ? n.offsetHeight : 0;

      // tổng chiều cao header + navbar
      const total = hH + nH;
      document.documentElement.style.setProperty('--top-offset', `${total}px`);
    };
    //cộng lại rồi ghi vào biến CSS --top-offset trên :root
    setTopOffset();
    window.addEventListener('resize', setTopOffset);
    const id = setInterval(setTopOffset, 300); 
    return () => { window.removeEventListener('resize', setTopOffset); clearInterval(id); };
  }, []);
  //Khai báo Router & Routes
  return (
    //bao ngoài toàn app.
    <Router> 
      <div className="app-container">
        {/* Truyền lang và setLang xuống Header */}
        <Header lang={lang} setLang={setLang} user={user} setUser={setUser}/>  
        <Navbar lang={lang}/>
        {/*đặt padding-top bằng biến --top-offset đã tính ở trên → nội dung đứng ngay dưới header+navbar.*/}
        <main className="page-content" style={{ paddingTop: 'var(--top-offset, 0px)'}}>
          <Routes>
            <Route path="/" element={<HomePage lang={lang} />} />
            <Route path="/benchan" element={<BenPage lang={lang} />} />
            <Route path="/lawyer" element={<LawyerPage lang={lang} />} />
            <Route path="/login" element={<LoginPage lang={lang} setUser={setUser} />} />
            <Route path="/register" element={<RegisterPage lang={lang} setUser={setUser} />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;