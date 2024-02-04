import { React, useEffect, useState } from 'react';
 import { useNavigate, useLocation } from 'react-router-dom';
import '../App.css';
import DataTable from './Table';

function Home() {
    const navigate = useNavigate();

    const location = useLocation();
    const username = location.state ? location.state.username : null;
    const classes = location.state ? location.state.classes : null;
    const school = location.state ? location.state.school : null;

    const [selectedClass, setSelectedClass] = useState('');
    const [studentNames, setStudentNames] = useState([]);
    const onLogout = (e) => { 
        e.preventDefault();
        navigate("/");
    }

    const handleSelectChange = async (event) => {
      setSelectedClass(event.target.value);
      var className = event.target.value;
      console.log("Selected class: " + className);
      // TODO: fetch the data for the selected class
      // then update the data table!
      const response = await fetch('/api/get-students', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({class: className, school: school}),
      });

      if (response.ok) {
          const data = await response.json();
          console.log(data);
          setStudentNames(data.students);
      }
    };

    return (
      <div className="Home">
        <h2>My Dashboard</h2>
        <h4>Classes:</h4>
        <select value={selectedClass} onChange={handleSelectChange}>
            <option value="" disabled select>Select a class</option>
            {classes.map((className, index) => (
                <option key={index} value={className}>
                    {className}
                </option>
            ))}
        </select>
        {selectedClass && 
          <p>Selected: {selectedClass}
            <DataTable data={studentNames} />
          </p>}
        
        <form>
          <p>
          <button onClick={onLogout}>Logout</button>
          </p>
        </form>
      </div>
    );
  };
  
export default Home;