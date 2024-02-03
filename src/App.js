import './App.css';
import { Routes, Route } from "react-router-dom"
import Home from './pages/Home';
import Login from './pages/Login';
import Student from './pages/Student';

function App() {
  const a = fetch("/api")
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