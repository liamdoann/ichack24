import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import StudentInfo from './StudentInfo';

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
        }
    } 
        fetchStudentData();
    }, []);

    // upon submit: call submit-report, and then pass the report, alongside username and classes to the report page
    

  return (
      <div>
          <h2>Student Details</h2>
          <p>Name: {name}</p>
          <p>Average: {average}</p>
          <p>Average Change: {avgDelta}</p>

          <StudentInfo posOrder={positiveOrder} negOrder={negativeOrder} imOrder={improvementOrder} name={name} className={className} school={school} username={username} classes={classes} />
      </div>
  );
}

export default Student;