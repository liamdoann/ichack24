import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import Info from './Info';

function StudentInfo({ posOrder, negOrder, imOrder, name, className, school, username, classes }) {
  const navigate = useNavigate();

  const { state } = useLocation();

  const [im, setIm] = useState('');
  const [itIm, setItIm] = useState([]);
  const [pos, setPos] = useState('');
  const [posIm, setPosIm] = useState([]);
  const [neg, setNeg] = useState('');
  const [negIm, setNegIm] = useState([]);
  const [score, setScore] = useState(3);

  console.log(posOrder);
  console.log(negOrder);
  console.log(imOrder);

  const handleScoreSubmit = (e) => {
    e.preventDefault();
    const data = new FormData(e.target);

    setScore(data.get('score'));
  }

  const handleFormSubmit = async () => {

    console.log(posIm);
    const positives = posIm.map((item) => item);
    const negatives = negIm.map((item) => item);
    const improvements = itIm.map((item) => item);
    console.log(positives);

    const response = await fetch('/api/submit-report', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ student: name, className: className, score: score, school: school, positiveComments: positives, negativeComments: negatives, improvementComments: improvements}),
    });

    if (response.ok) {
        const data = await response.json();
        console.log(data);
        navigate("/report", { state: { username : username, classes: classes, school: school, report: data.report } });
    }
  }

  return (
    <div>
      <Info title={"Improvements"} text={im} setText={setIm} items={itIm} setItems={setItIm} quotes={imOrder} />
      <Info title={"Positives"} text={pos} setText={setPos} items={posIm} setItems={setPosIm} quotes={posOrder} />
      <Info title={"Negatives"} text={neg} setText={setNeg} items={negIm} setItems={setNegIm} quotes={negOrder} />
      
      <h3>Overall Score</h3>
      <p style={{fontSize:'10pt'}}>Give them a rating from 1 to 5...</p>
      <form onSubmit={handleScoreSubmit}>
        <div style={{fontSize: '14pt', display:'flex', width:'50%', justifyContent: 'space-between'}}>
        <label>
          1<input type="radio" name="score" value="1"></input>
        </label>
        <label>
        2<input type="radio" name="score" value="2"></input>
        </label>
        <label>
        3<input type="radio" name="score" value="3"></input>
        </label>
        <label>
        4<input type="radio" name="score" value="4"></input>
        </label>
        <label>
        5<input type="radio" name="score" value="5"></input>
        </label>
        </div>

        <br></br>
      </form>
      <button class="report-button"  onClick={handleFormSubmit}>Generate report</button>
    </div>
  );
}

export default StudentInfo;