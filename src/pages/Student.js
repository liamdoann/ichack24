import React from 'react';
import { useNavigate, useLocation, useParams } from 'react-router-dom';

function Student() {
  const { state } = useLocation();

  return (
      <div>
          <h2>Student Details</h2>
          <p>Name: {state.Name}</p>
          <p>Age: {state.Age}</p>
          <p>Occupation: {state.Occupation}</p>
      </div>
  );
}

export default Student;