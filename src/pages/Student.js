import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import StudentInfo from './StudentInfo';
import TopBar from './TopBar';

function Student() {
    const navigate = useNavigate();

    const location = useLocation();
    const state = location.state ? location.state : null;
    const name = state ? state.name : null;
    const school = state ? state.school : null;
    const className = state ? state.className : null;
    const username = state ? state.username : null;
    const classes = state ? state.classes : null;

    const [lastImprovements, setLastImprovements] = useState([]);
    const [percentages, setPercentages] = useState([]);
    const [average, setAverage] = useState(0);
    const [avgDelta, setAvgDelta] = useState(0);
    const [positiveOrder, setPositiveOrder] = useState([]);
    const [negativeOrder, setNegativeOrder] = useState([]);
    const [improvementOrder, setImprovementOrder] = useState([]);
    const [classAverage, setClassAverage] = useState(0);

    useEffect(() => {
    const fetchStudentData = async () => {
        const response = await fetch('/api/find-student', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({student: name, class: className, school: school}),
        });

        if (response.ok) {
            const data = await response.json();
            console.log(data);
            setLastImprovements(data.lastImprovements);
            setPercentages(data.percentages);
            setAverage(data.average);
            setAvgDelta(data.avgDelta);
            setPositiveOrder(data.positiveOrder);
            setNegativeOrder(data.negativeOrder);
            setImprovementOrder(data.improvementOrder);  
            setClassAverage(data.classAverage); 
        }
    } 
        fetchStudentData();
    }, []);

    // upon submit: call submit-report, and then pass the report, alongside username and classes to the report page
    

  return (
    <>
    <TopBar />
      <div className="content-below">
        <div className="inner-content">
          <h2>Student Details</h2>
          <p style={{fontSize: '20pt'}}>Class: {className} | Average: {classAverage}</p>
          <p style={{fontSize: '20pt'}}>Name: {name}<br/>Average: {average}<br/>Average Change: {avgDelta}</p>
          <StudentInfo posOrder={positiveOrder} negOrder={negativeOrder} imOrder={improvementOrder} name={name} className={className} school={school} username={username} classes={classes} />
        </div>
      </div>
      </>
  );
}

export default Student;