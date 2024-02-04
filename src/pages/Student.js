import React from 'react';
import { useLocation } from 'react-router-dom';
import StudentInfo from './StudentInfo';

function Student() {
    const { state } = useLocation();

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