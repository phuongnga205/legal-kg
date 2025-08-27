import React from 'react';
import { Link } from 'react-router-dom';
import ChatBox from '../components/ChatBox';
import Overlay from "../components/Overlay.jsx";

const BenPage = ({ lang, user }) => {
  return (
    <div className="benchan-page">
      <ChatBox lang={lang} />
      {!user && <Overlay lang={lang} />}
    </div>
  );
};

export default BenPage;
