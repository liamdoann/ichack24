import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import Info from './Info';

function StudentInfo({ posOrder, negOrder, imOrder}) {
  const { state } = useLocation();

  const [im, setIm] = useState('');
  const [itIm, setItIm] = useState([]);
  const [pos, setPos] = useState('');
  const [posIm, setPosIm] = useState([]);
  const [neg, setNeg] = useState('');
  const [negIm, setNegIm] = useState([]);

  const [displayText, setDisplayText] = useState('');

  const handleClick = () => {
    setDisplayText(`${state} -- Negative: ${negIm}, Positive: ${posIm}, It: ${itIm}`);
  };

  return (
    <div>
      <Info title={"Improvements"} text={im} setText={setIm} items={itIm} setItems={setItIm} quotes={imOrder} />
      <Info title={"Positives"} text={pos} setText={setPos} items={posIm} setItems={setPosIm} quotes={posOrder} />
      <Info title={"Negatives"} text={neg} setText={setNeg} items={negIm} setItems={setNegIm} quotes={negOrder} />

      <button onClick={handleClick}>Display Text</button>
      <p>{displayText}</p>
    </div>
  );
}

export default StudentInfo;