import React from 'react';
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
        <div id="rcorners2" style={{height:'400px'}}>
        <img src={eduPlanner} alt="EduPlanner Logo" style={{ width: '220px' }}/>
            
            <form onSubmit={handleSubmit}>
                <p>
                    <h4>Please login to continue</h4>
                    <input type="text" name="username" placeholder="username" required/>
                    <input type="password" name="password" placeholder="password" required/>
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