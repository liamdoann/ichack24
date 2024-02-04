import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import StudentInfo from './StudentInfo';

function Student() {

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

    const data = async () => {
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

    // upon submit: call submit-report, and then pass the report, alongside username and classes to the report page

  return (
      <div>
          <h2>Student Details</h2>
          <p>Name: {state.Name}</p>
          <p>Age: {state.Age}</p>
          <p>Occupation: {state.Occupation}</p>

          <StudentInfo/>
      </div>
  );
}

export default Student;