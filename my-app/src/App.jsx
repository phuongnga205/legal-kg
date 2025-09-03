import React, { useEffect, useState } from 'react';   
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Header from './components/Header';
import Navbar from './components/Navbar';
import HomePage from './pages/HomePage';
import BenPage from './pages/BenPage';
import LawyerPage from './pages/LawyerPage'; 
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import './App.css';

// 🔒 Route bảo vệ
function ProtectedRoute({ user, children }) {
  if (!user) {
    return <Navigate to="/login" replace />;
  }
  return children;
}

function App() {
  const [lang, setLang] = useState("EN"); 
  const [user, setUser] = useState(null);  

  // 🔑 Load user từ localStorage khi F5
  useEffect(() => {
    const saved = localStorage.getItem("user");
    if (saved) {
      setUser(JSON.parse(saved));
    }
  }, []);

  // 🔑 Logout
  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem("user");
  };

  // Khi login/register thành công → lưu localStorage
  const handleSetUser = (u) => {
    setUser(u);
    localStorage.setItem("user", JSON.stringify(u));
  };

  // Tính khoảng đệm dưới header + navbar
  useEffect(() => {
    const setTopOffset = () => {
      const h = document.querySelector('.header');
      const n = document.querySelector('.navbar');
      const hH = h ? h.offsetHeight : 0;
      const nH = n ? n.offsetHeight : 0;
      const total = hH + nH;
      document.documentElement.style.setProperty('--top-offset', `${total}px`);
    };
    setTopOffset();
    window.addEventListener('resize', setTopOffset);
    const id = setInterval(setTopOffset, 300); 
    return () => { 
      window.removeEventListener('resize', setTopOffset); 
      clearInterval(id); 
    };
  }, []);

  return (
    <Router> 
      <div className="app-container">
        <Header 
          lang={lang} 
          setLang={setLang} 
          user={user} 
          setUser={setUser} 
          onLogout={handleLogout} 
        />  
        <Navbar lang={lang} />

        <main className="page-content" style={{ paddingTop: 'var(--top-offset, 0px)'}}>
          <Routes>
            <Route path="/" element={<HomePage lang={lang} />} />
            
            {/* 🔒 Trang yêu cầu đăng nhập */}
            <Route path="/benchan" element={<BenPage lang={lang} user={user} />} />
            <Route path="/lawyer" element={<LawyerPage lang={lang} user={user} />} />  
            {/*<Route 
              path="/lawyer" 
              element={
                <ProtectedRoute user={user}>
                  <LawyerPage lang={lang} />
                </ProtectedRoute>
              } 
            />*/}
            

            <Route path="/login" element={<LoginPage lang={lang} setUser={handleSetUser} />} />
            <Route path="/register" element={<RegisterPage lang={lang} setUser={handleSetUser} />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
