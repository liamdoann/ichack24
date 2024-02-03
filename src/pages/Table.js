import React from 'react';
import { useNavigate } from 'react-router-dom';

// npm install @coreui/react-chartjs

function DataTable({ data }) {
  const navigate = useNavigate();
  const headers = data.length > 0 ? Object.keys(data[0]) : [];

  const handleRowClick = (rowData) => {
    navigate(`/student/${rowData.id}`, { state: rowData });
};

  return (
      <table>
          <thead>
              <tr>
                  {headers.map((header, index) => (
                      <th key={index}>{header}</th>
                  ))}
              </tr>
          </thead>
          <tbody>
              {data.map((row, rowIndex) => (
                  <tr key={rowIndex} onClick={() => handleRowClick(row)}>
                      {headers.map((header, columnIndex) => (
                          <td key={columnIndex}>{row[header]}</td>
                      ))}
                  </tr>
              ))}
          </tbody>
      </table>
  );
}

export default DataTable;