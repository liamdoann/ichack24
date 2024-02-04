import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function DataTable({ data, school, className, username, classes }) {
  const [search, setSearch] = useState('');

  const navigate = useNavigate();
  const headers = data.length > 0 ? Object.keys(data[0]) : [];

  const filteredData = data.filter(row => 
    row.Name.toLowerCase().includes(search.toLowerCase())
  );

  const handleRowClick = (rowData) => {
    console.log(rowData)
    navigate(`/student/`, { state: {name: rowData.Name, school: school, className: className, username: username, classes: classes} });
    };

  return (
    <div>
    <input 
        style={{width:'100%', marginBottom: '10px'}}
        type="text" 
        value={search} 
        onChange={e => setSearch(e.target.value)} 
        placeholder="Search..."
      />
    <div class="table-container">
      <table>
          <thead>
              <tr>
                  {headers.map((header, index) => (
                      <th key={index}>{header}</th>
                  ))}
              </tr>
          </thead>
          <tbody>
              {filteredData.map((row, rowIndex) => (
                  <tr key={rowIndex} onClick={() => handleRowClick(row)}>
                      {headers.map((header, columnIndex) => (
                          <td key={columnIndex}>{row[header]}</td>
                      ))}
                  </tr>
              ))}
          </tbody>
      </table>
    </div>
    </div>
  );
}

export default DataTable;