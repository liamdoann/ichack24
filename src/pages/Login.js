import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import eduPlanner from './eduplanner.png';

function Login() {
    const navigate = useNavigate();

    const handleSubmit = (e) => { 
        e.preventDefault();
        const data = new FormData(e.target);
        navigate("/home", { state: { username: data.get('username') } });
    }

    return (
      <div className="Login">
        <div id="rcorners2">
        <img src={eduPlanner} alt="EduPlanner Logo" style={{ width: '300px' }}/>
            <h4>Sign in to use</h4>
            <form onSubmit={handleSubmit}>
                <p>
                    <label>Username</label><br/>
                    <input type="text" name="username" required />
                </p>
                <p>
                    <label>Password</label>
                    <br/>
                    <input type="password" name="password" required />
                </p>
                <p>
                    <button type="submit">Login</button>
                </p>
            </form>
            </div>
        </div>
    );
  }

export default Login;