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

    const onLogout = (e) => { 
        e.preventDefault();
        navigate("/");
    }

    const handleSelectChange = (event) => {
      setSelectedClass(event.target.value);
      // TODO: fetch the data for the selected class
      // then update the data table!
    };

    const dummyData = [
      { id: "j1", Name: 'John', Age: 30, Occupation: 'Engineer' },
      { id: "j2", Name: 'Jane', Age: 28, Occupation: 'Doctor' },
  ];

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
            <DataTable data={dummyData} />
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