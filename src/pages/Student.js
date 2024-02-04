import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import StudentInfo from './StudentInfo';

function Student() {

    const location = useLocation();
    const name = location.state ? location.state.name : null;
    const school = location.state ? location.state.school : null;
    const className = location.state ? location.state.className : null;

    const [lastImprovements, setLastImprovements] = useState([]);
    const [percentages, setPercentages] = useState([]);
    const [average, setAverage] = useState(0);
    const [avgDelta, setAvgDelta] = useState(0);
    const [positiveOrder, setPositiveOrder] = useState([]);
    const [negativeOrder, setNegativeOrder] = useState([]);
    const [improvementOrder, setImprovementOrder] = useState([]);

    useEffect(() => {
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
                // use data {'lastImprovements': lastImprovements, 'percentages': percentages, 'average': average, 'avgDelta': avgDelta, 'positiveOrder': positiveOrder, 'negativeOrder': negativeOrder, 'improvementOrder': improvementOrder}
                setLastImprovements(data.lastImprovements);
                setPercentages(data.percentages);
                setAverage(data.average);
                setAvgDelta(data.avgDelta);
                setPositiveOrder(data.positiveOrder);
                setNegativeOrder(data.negativeOrder);
                setImprovementOrder(data.improvementOrder);   
            }
        };

        data();
    }, []);

  return (
      <div>
          <h2>Student Details</h2>
          <p>Name: {name}</p>
          <p>Age: {school}</p>
          <p>Occupation: {className}</p>

          <StudentInfo/>
      </div>
  );
}

export default Student;