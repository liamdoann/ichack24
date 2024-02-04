import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import TopBar from './TopBar';

function Report() {

    const navigate = useNavigate();

    const location = useLocation();
    const state = location.state ? location.state : null;
    const username = state ? state.username : null;
    const classes = state ? state.classes : null;
    const school = state ? state.school : null;
    const report = state ? state.report : null;


    const onReturn = (e) => {
        console.log(username);
        console.log(classes);
        console.log(school);
        e.preventDefault();
        navigate("/home", { state: { username : username, classes: classes, school: school } });
    }

  return (
    <>
        <TopBar />
        <div class="content-below">
            <div className="inner-content">
                <div className="Report" style={{width:'600pt'}}>
                    {report}
                    <br></br>
                    <form onSubmit={onReturn}>
                        <p>
                            <button type="submit">back</button>
                        </p>
                    </form>
                </div>
            </div>
        </div>
    </>
  );
}

export default Report;