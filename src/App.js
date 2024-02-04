import React, {useState, useEffect} from 'react';
import './App.css';
import { Routes, Route } from "react-router-dom"
import Home from './pages/Home';
import Login from './pages/Login';
import Student from './pages/Student';
import Report from './pages/Report';
import SeatingPlan from './pages/seatingPlan';
import PerformanceGraph from './pages/Graph';
import { LineChart } from '@mui/x-charts';

function App() {
    const [msg, setMsg] = useState([]);
    useEffect(() => {
        msgs();
    }, []);
    const msgs = async () => {
        const response = await fetch('/api/auth/login');
        const data = await response.json();
        console.log(response);
        setMsg(data);
    }

  return (
    <div className="App"> 
        <Routes>
          <Route path="/" element={ <Login/> }/>
          <Route path="/home" element={ <Home/> }/>
          <Route path="/student/" element={ <Student/> }/>
          <Route path="/report" element={ <Report/> }/>
          <Route path="/seatingPlan" element={ <SeatingPlan/> }/>
        </Routes>
    </div>
  );
}

export default App;