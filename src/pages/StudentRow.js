import React from 'react';

function StudentRow({ name, averageMark, averageChange }) {
  return (
    <div className="student-row">
      <div className="student-name">{name}</div>
      <div className="average-mark">{averageMark}</div>
      <div className={`average-change ${averageChange > 0 ? 'up' : averageChange < 0 ? 'down' : 'neutral'}`}>
        {averageChange > 0 ? '↑' : averageChange < 0 ? '↓' : '—'}
      </div>
    </div>
  );
}

export default StudentRow;