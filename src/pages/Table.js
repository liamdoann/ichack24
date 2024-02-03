import React from 'react';

function DataTable({ data }) {
    // Get the keys of the first object in the data array to use as column headers
    const headers = data.length > 0 ? Object.keys(data[0]) : [];

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
                    <tr key={rowIndex}>
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