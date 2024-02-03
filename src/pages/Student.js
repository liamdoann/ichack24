import React from 'react';
import { useNavigate } from 'react-router-dom';

function Student() {
  const navigate = useNavigate();

    const onLogout = (e) => { 
        e.preventDefault();
        console.log("hello");
        navigate("/");
    }

    return (
      <div className="Home">
        <h2>Welcome!</h2>
        <form>
          <p>
          <button onClick={onLogout}>Back</button>
          </p>
        </form>
      </div>
    );
  };
  
export default Home;