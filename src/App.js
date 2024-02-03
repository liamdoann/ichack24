import './App.css';
import { Routes, Route } from "react-router-dom"
import Home from './pages/Home';
import Login from './pages/Login';

function App() {
  return (
    <div className="App">
        <Routes>
          <Route path="/" element={ <Login/> }/>
          <Route path="/home" element={ <Home/> }/>
        </Routes>
    </div>
  );
}

export default App;