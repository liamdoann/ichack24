import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

function Report() {

    const location = useLocation();
    const state = location.state ? location.state : null;
    const username = state ? state.username : null;
    const classes = state ? state.classes : null;
    const school = state ? state.school : null;
    const report = state ? state.report : null;

    // show report on page
    // call ' navigate("/home", { state: { username : username, classes: classes, school: school } }); '
    // after pressing return button

  return (
      <div>{report}</div>
  );
}

export default Report;