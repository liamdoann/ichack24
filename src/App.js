import React, {useState, useEffect} from 'react';
import logo from './logo.svg';
import './App.css';
import { Routes, Route } from "react-router-dom"
import Home from './pages/Home';
import Login from './pages/Login';
import Student from './pages/Student';

function App() {
    const [msg, setMsg] = useState([]);
    useEffect(() => {
        msgs();
    }, []);
    const msgs = async () => {
        const response = await fetch('/auth/login');
        const data = await response.json();
        setMsg(data);
    }

  return (
    <div className="App">
        <Routes>
          <Route path="/" element={ <Login/> }/>
          <Route path="/home" element={ <Home/> }/>
          <Route path="/student/:id" element={ <Student/> }/>
        </Routes>
    </div>
  );
}

export default App;