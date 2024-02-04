import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import './Seating.css';


function SeatingPlan({ seatingPlanData }) {

    const [grid, setGrid] = useState([]);

    useEffect(() => {
        // Extract unique row and column values from the seating plan
        const rows = [...new Set(Object.values(seatingPlanData).map(item => item.x))];
        const columns = [...new Set(Object.values(seatingPlanData).map(item => item.y))];

        // Create a 2D grid with empty cells
        const newGrid = Array.from({ length: rows.length }, () =>
            Array.from({ length: columns.length }, () => null)
        );

        // Populate the grid with student names at their coordinates
        Object.entries(seatingPlanData).forEach(([name, coordinates]) => {
            const rowIndex = rows.indexOf(coordinates.x);
            const colIndex = columns.indexOf(coordinates.y);
            newGrid[rowIndex][colIndex] = name;
        });

        setGrid(newGrid);
    }, []);

    return (
        <div className="Seating Plan">
        <h2>Generated Seating Plan:</h2>
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
        <div style={{textAlign: 'center'}}><h3 style={{textAlign: 'center'}}>Front</h3></div>
        
        </div>
    );
};

export default SeatingPlan;