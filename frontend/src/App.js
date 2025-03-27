import React, { useRef } from "react";   
import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import '@fortawesome/fontawesome-free/css/all.min.css';
import Navbar from './Components/Navbar';
import HomePage from './Components/Home';
import Apage from './Components/Ab';
import Upload from './Components/Upload';
// import Formm from './Components/Formm';
// import AIChatbotResult from './Components/AIBotResult';

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/about" element={<Apage />} />
        <Route path="/upload" element={<Upload />} />
        {/* <Route path="/form" element={<Formm />} /> */}
        {/* <Route path="/chatbot" element={<AIChatbotResult />} /> */}
      </Routes>
    </Router>
  );
}

export default App;
