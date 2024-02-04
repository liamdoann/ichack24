import React, { useState } from 'react';
import Info from './Info';

function StudentInfo() {
  const [im, setIm] = useState('');
  const [itIm, setItIm] = useState([]);
  const [pos, setPos] = useState('');
  const [posIm, setPosIm] = useState([]);
  const [neg, setNeg] = useState('');
  const [negIm, setNegIm] = useState([]);

  const [displayText, setDisplayText] = useState('');

  const handleClick = () => {
    setDisplayText(`Negative: ${negIm}, Positive: ${posIm}, It: ${itIm}`);
  };

  return (
    <div>
      <Info title={"Improvements"} text={im} setText={setIm} items={itIm} setItems={setItIm} />
      <Info title={"Positives"} text={pos} setText={setPos} items={posIm} setItems={setPosIm} />
      <Info title={"Negatives"} text={neg} setText={setNeg} items={negIm} setItems={setNegIm} />

      <button onClick={handleClick}>Display Text</button>
      <p>{displayText}</p>
    </div>
  );
}

export default StudentInfo;