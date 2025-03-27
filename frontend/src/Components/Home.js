
import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

function Home() {
  return (
    <div className="home-container">
      <h1 className="home-title">Welcome to Skin Disease Analyzer</h1>
      <Link to="/upload"><button className="home-button">Get Started</button></Link>
      
    </div>
  );
}

export default Home;
