import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Navbar from './components/Navbar';
import HomePage from './pages/HomePage';
import BenPage from './pages/BenPage';
import './App.css'; // Quan trọng

function App() {
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