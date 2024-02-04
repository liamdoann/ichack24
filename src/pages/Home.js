import { React, useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import '../App.css';
import DataTable from './Table';
import TopBar from './TopBar';

function Home() {
    

    const location = useLocation();
    const username = location.state ? location.state.username : null;
    const classes = location.state ? location.state.classes : null;
    const school = location.state ? location.state.school : null;

    console.log(classes);

    const [selectedClass, setSelectedClass] = useState('');
    const [studentNames, setStudentNames] = useState([]);
    const [isSelected, setIsSelected] = useState(false);
    

    const handleSelectChange = async (event) => {
      setIsSelected(true);
      setSelectedClass(event.target.value);
      var className = event.target.value;
      console.log("Selected class: " + className);
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
      <>
      <TopBar /> 
        <div class="content-below">
        <div className="Home">
          <div className="flexHeader">
            <h2>Welcome, {username}!</h2>
          </div>

          <select value={selectedClass} onChange={handleSelectChange}>
            <option value="" disabled select>Select a class</option>
            {classes.map((className, index) => (
              <option key={index} value={className}>
                {className}
              </option>
            ))}
          </select>

          {!isSelected && <p>Please select a class above to continue.</p>}
          {selectedClass &&
            <p>
              <DataTable data={studentNames} school={school} className={selectedClass} username={username} classes={classes} />
            </p>}
          </div>
        </div>
      </>
    );
  };
  
export default Home;