import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import eduPlanner from './eduplanner.png';

function Login() {
    const navigate = useNavigate();
    
    const handleSubmit = async (e) => { 
        e.preventDefault();

        const data = new FormData(e.target);
        const username = data.get('username');
        const password = data.get('password');

        const response = await fetch('/api/validate-login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password}),
        });

        if (response.ok) {
            const data = await response.json();

            if (data.success) {
                navigate("/home", { state: { username : username, classes: data.classes, school: data.school } });
            } else {
                alert("Invalid credentials.");
            }
        } 
    }

    return (
      <div className="Login">
        <div id="rcorners2" style={{height:'400px'}}>
        <img src={eduPlanner} alt="EduPlanner Logo" style={{ width: '220px' }}/>

            <form onSubmit={handleSubmit}>
                <p style={{paddingBottom:'10pt'}}>
                    <h4 style={{marginBottom: '10px'}}>Please login to continue</h4>
                    <input type="text" name="username" placeholder="username" required/>
                    <input type="password" name="password" placeholder="password" required/>
                    <button type="submit" style={{marginTop: '15px'}}>Login</button>
                </p>
                <p style={{fontSize:'8pt', paddingTop:'10pt', color:'grey'}}>
                   Made with love by SCR Table 15. 
                </p>
            </form>
            </div>
        </div>
    );
}

export default Login;