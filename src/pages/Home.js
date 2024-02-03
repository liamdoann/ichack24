// import React from 'react';
import { React, useEffect, setEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../App.css';
import DataTable from './Table';

function Home() {
    const navigate = useNavigate();

    const [classes, setClasses] = useState([]);
    const [selectedClass, setSelectedClass] = useState('');
  
    useEffect(() => {
      // fetch('/get-classes')
      //     .then(response => response.json())
      //     .then(data => setClasses(data.classes));
      const dummyClasses = ['Year 10 Maths', 'Year 11 Physics', 'Year 12 Chemistry'];
      setClasses(dummyClasses);
    }, []);

    const onLogout = (e) => { 
        e.preventDefault();
        console.log("hello");
        navigate("/");
    }

    const handleSelectChange = (event) => {
      setSelectedClass(event.target.value);
      // TODO: fetch the data for the selected class
      // then update the data table!
    };

    const dummyData = [
      { Name: 'John', Age: 30, Occupation: 'Engineer' },
      { Name: 'Jane', Age: 28, Occupation: 'Doctor' },
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