import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

function Report() {

    const navigate = useNavigate();

    const location = useLocation();
    const state = location.state ? location.state : null;
    const username = state ? state.username : null;
    const classes = state ? state.classes : null;
    const school = state ? state.school : null;
    const report = state ? state.report : null;


    const onReturn = (e) => {
        e.preventDefault();
        navigate("/home", { state: { username : username, classes: classes, school: school } });
    }

  return (
    <div className="Report">
        {report}
        <br></br>
        <form onSubmit={onReturn}>
            <p>
                <button type="submit">back</button>
            </p>
        </form>
    </div>
  );
}

export default Report;