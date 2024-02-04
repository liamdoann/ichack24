import { React, useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import '../App.css';
import DataTable from './Table';
import TopBar from './TopBar';
import SeatingPlan from './SeatingPlan'

function processIntPairs(inputString) {
    let result = {};
  
    let tuples = inputString.split(';');
  
    tuples.forEach(tuple => {
      let elements = tuple.substring(1, tuple.length - 1).split(',');
  
      if (result[elements[0]] === undefined) {
        result[elements[0]] = [parseInt(elements[1])];
      } else {
        result[elements[0]].push(parseInt(elements[1]));
      }
    });
  
    return result;
  }

function processStringPairs(inputString) {
    let result = {};
  
    let tuples = inputString.split(';');
  
    tuples.forEach(tuple => {
      let elements = tuple.substring(1, tuple.length - 1).split(',');
  
      if (result[elements[0]] === undefined) {
        result[elements[0]] = [elements[1]];
      } else {
        result[elements[0]].push(elements[1]);
      }
    });
  
    return result;
  }

function Home() {
    const handleSubmit = async (e) => { 
        e.preventDefault();
        const data = new FormData(e.target);
        const desks_data = data.get('desks');
        const at_front_data = data.get('at_front');
        const keep_separate_data = data.get('keep_separate');

        const desks = processIntPairs(desks_data);
        const at_front = at_front_data.split(";");
        const keep_separate = processStringPairs(keep_separate_data);
        const students = Object.keys(studentNames).map(key => studentNames[key]['Name']);

        const response = await fetch('/api/get-seating-plan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({desks : desks, students: students, at_front : at_front, keep_separate : keep_separate})
        });

        if (response.ok) {
            const data = await response.json();
            if (data.success) {
                setSeatingPlan(data.result);
                setSeatingPlanSuccess(true);
            } else {
                alert("No suitable seating plan could be generated. Please edit your criteria.");
            }
        } 
    }

    const location = useLocation();
    const username = location.state ? location.state.username : null;
    const classes = location.state ? location.state.classes : null;
    const school = location.state ? location.state.school : null;

    console.log(classes);

    const [selectedClass, setSelectedClass] = useState('');
    const [studentNames, setStudentNames] = useState([]);
    const [isSelected, setIsSelected] = useState(false);
    const [seatingPlanSuccess, setSeatingPlanSuccess] = useState(false);
    const [seatingPlan, setSeatingPlan] = useState({});
    
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
            <h2>Welcome, <span style={{color: '#019472', fontWeight:'bold'}}>{username}</span>!</h2>

            <select value={selectedClass} onChange={handleSelectChange}>
            <option value="" disabled select>Select a class</option>
            {classes.map((className, index) => (
              <option key={index} value={className}>
                {className}
              </option>
            ))}
          </select>
          </div>

          <p style={{fontSize:'12pt'}}>After selecting a class above, click on a student in the table to navigate to the information view.
             There, you'll be able to generate a report using data from previous reports and positive/negative/improvement comments.
          </p>

          

          {!isSelected && <p style={{alignContent:'center', color:'gray', fontSize:'10pt'}}>Please select a class above to continue.</p>}
          {selectedClass &&
            <p>
              <DataTable data={studentNames} school={school} className={selectedClass} username={username} classes={classes} />
            </p>}
          {selectedClass && 
            <div>
                <h2 style={{marginBlockStart:'30pt'}}>Generate Classroom Seating Plan</h2>
                <form onSubmit={handleSubmit}>
                <p>
                    <h3 style={{marginBottom: '10px'}}>Enter coordinates corresponding to your classroom layout (format: (x1,y1);(x2,y2);...). </h3>
                    <input type="desks" name="desks" placeholder=""/>
                    <h3 style={{marginBottom: '10px'}}> Enter students you would like to seat in the front row (format: A;B;C;...). </h3>
                    <input type="at_front" name="at_front" placeholder=""/>
                    <h3 style={{marginBottom: '10px'}}>Enter pairs of students you would like to seat apart from each other (format: (A,B); (C,D);...):</h3>
                    <input type="keep_separate" name="keep_separate" placeholder=""/>
                    <br></br>
                    <button type="submit" style={{marginTop: '15px'}}>Submit</button>
                </p>
                <p>
                    {seatingPlanSuccess && <SeatingPlan seatingPlanData ={seatingPlan}/>}
                </p>
            </form>
            </div>
            }
          </div>
        </div>
      </>
    );
  };
  
export default Home;