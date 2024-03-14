import React from "react";
import { CircularProgress, Typography } from "@mui/material";
import "./CsvTable.css"; // Import CSS file for styling

const LoadingSpinner = () => {
  return (
    <div className="loading-container">
      <CircularProgress size={24} color="primary" />
      <Typography variant="body2" size={12} className="loading-message">
        Loading data ...
      </Typography>
    </div>
  );
};

export default LoadingSpinner;
