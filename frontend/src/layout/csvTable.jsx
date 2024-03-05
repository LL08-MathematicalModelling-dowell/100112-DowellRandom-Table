import React from "react";
import "./CsvTable.css"; // Import CSS file for styling

const CsvTable = ({ data }) => {
  return (
    <div className="csv-table-container">
      <table className="csv-table">
      <thead>
        <tr>
          {data.length > 0 &&
            data[0].map((header, index) => (
              <th key={index}>Field {index + 1}</th>
            ))}
        </tr>
      </thead>
        <tbody>
          {data.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {row.map((cell, cellIndex) => (
                <td key={cellIndex}>{cell}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default CsvTable;
