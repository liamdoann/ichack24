import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Login() {
    const navigate = useNavigate();

    const handleSubmit = (e) => { 
        e.preventDefault();
        const data = new FormData(e.target);
        navigate("/home", { state: { username: data.get('username') } });
    }

    return (
      <div className="Login">
        <h1>
          EduPlanner
        </h1>
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
    );
  }

export default Login;