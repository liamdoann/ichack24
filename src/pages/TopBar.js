import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import eduPlanner from './eduplanner-nt.png';

export default function TopBar() {
  const navigate = useNavigate();

  const onLogout = (e) => { 
    e.preventDefault();
    navigate("/");
}

  return (
    <div class="top-bar">
      <div class="top-bar-content">
        <img src={eduPlanner} alt="EduPlanner Logo" style={{ width: '130px' }}/>
        <button class="bar-button" onClick={onLogout} style={{ width: '60px' }}>Logout</button>
      </div>
    </div> 
  )
}