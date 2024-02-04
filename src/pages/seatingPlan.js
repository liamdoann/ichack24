import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import './Seating.css';

const seatingPlanData = {
  'student1': { 'y': 1, 'x': 1 },
  'student2': { 'y': 2, 'x': 3 },
  'student3': { 'y': 3, 'x': 2 },
  // Add more students and coordinates as needed
};

function SeatingPlan() {

    const navigate = useNavigate();
    const location = useLocation();
    const state = location.state ? location.state : null;
    const seatingPlanData = state ? state.grid : null;

    const [grid, setGrid] = useState([]);

    useEffect(() => {
        // Extract unique row and column values from the seating plan
        const rows = [...new Set(Object.values(seatingPlanData).map(item => item.y))];
        const columns = [...new Set(Object.values(seatingPlanData).map(item => item.x))];

        // Create a 2D grid with empty cells
        const newGrid = Array.from({ length: rows.length }, () =>
            Array.from({ length: columns.length }, () => null)
        );

        // Populate the grid with student names at their coordinates
        Object.entries(seatingPlanData).forEach(([name, coordinates]) => {
            const rowIndex = rows.indexOf(coordinates.y);
            const colIndex = columns.indexOf(coordinates.x);
            newGrid[rowIndex][colIndex] = name;
        });

        setGrid(newGrid);
    }, []);

    return (
        <div className="App">
        <h1>Seating Plan</h1>
        <div className="grid-container">
        <div className="grid">
            {grid.map((row, rowIndex) => (
            <div key={rowIndex} className="row">
                {row.map((studentName, colIndex) => (
                <div key={colIndex} className="cell">
                    {studentName && <span>{studentName}</span>}
                </div>
                ))}
            </div>
            ))}
        </div>
        </div>
        </div>
    );
};

export default SeatingPlan;