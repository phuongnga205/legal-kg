import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Navbar from './components/Navbar';
import HomePage from './pages/HomePage';
import BenPage from './pages/BenPage';
import './App.css';

function App() {
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

    setTopOffset();
    // cập nhật khi resize hoặc font/load ảnh làm đổi chiều cao
    window.addEventListener('resize', setTopOffset);
    const id = setInterval(setTopOffset, 300); // đảm bảo sau khi CSS/ảnh load
    return () => { window.removeEventListener('resize', setTopOffset); clearInterval(id); };
  }, []);

  return (
    <Router>
      <div className="app-container">
        <Header />
        <Navbar />
        <div className="page-content">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/benchan" element={<BenPage />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;