import React from 'react';
import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import '@fortawesome/fontawesome-free/css/all.min.css';
import HomePage from './Components/Home';
import Upload from './Components/Upload';
import Formm from './Components/Formm';
import Navbar from './Components/Navbar';
// import AIChatbotResult from './Components/AIBotResult';
import Apage from './Components/Ab';

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/upload" element={<Upload />} />
        <Route path="/form" element={<Formm />} />
        <Route path="/about" element={<Apage />} />
        <Route path="/chatbot" element={<AIChatbotResult />} />
      </Routes>
    </Router>
  );
}

export default App;
