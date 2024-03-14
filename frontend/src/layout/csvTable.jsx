import * as React from 'react';
import { DataGrid } from '@mui/x-data-grid';
import "./CsvTable.css";

const DataTable = ({ data }) => {
  const getRowClassName = React.useCallback((params) => {
    return `super-app-theme--row`;
  }, []);

  const columns = data.length > 0 ? data[0].map((header, index) => ({
    field: `field${index + 1}`,
    headerName: `Field ${index + 1}`,
    flex: 1,
    headerClassName: 'super-app-theme--header', // Add this line
  })) : [];

  const rows = data.map((row, rowIndex) => ({
    id: rowIndex + 1,
    ...row.reduce((acc, cell, cellIndex) => ({
      ...acc,
      [`field${cellIndex + 1}`]: cell
    }), {})
  }));

  return (
    <div className="csv-table-container">
      <div style={{ height: 400, width: '100%' }}>
        <DataGrid
          rows={rows}
          columns={columns}
          getRowClassName={getRowClassName} // Apply custom row styles using getRowClassName
          initialState={{
            pagination: {
              paginationModel: { page: 0, pageSize: 5 },
            },
          }}
          pageSizeOptions={[5, 10]}
        />
      </div>
    </div>
  );
};

export default DataTable;
