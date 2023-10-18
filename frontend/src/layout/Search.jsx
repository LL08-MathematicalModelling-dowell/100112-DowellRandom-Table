import React, { useState } from 'react';
import {
  TextField,
  Select,
  MenuItem,
  InputLabel,
  FormControl,
  Box,
  Button,
  CircularProgress,
} from '@mui/material';

const Search = () => {
  const [field, setField] = useState('field1');
  const [regex, setRegex] = useState('');
  const [size, setSize] = useState('');
  const [position, setPosition] = useState('');
  const [isSearching, setIsSearching] = useState(false);

  const jsonToCsv = (jsonData) => {
    let csv = '';
    let headers = Object.keys(jsonData[0]);
    csv += headers.join(',') + '\n';
    jsonData.forEach(function (row) {
        let data = headers.map(header => JSON.stringify(row[header])).join(','); 
        csv += data + '\n';
    });
    return csv;
  }

  const downloadCsvfile = (data) => {
    let csvData = jsonToCsv(data);
    let blob = new Blob([csvData], { type: 'text/csv' });
    let url = window.URL.createObjectURL(blob);
    let a = document.createElement('a');
    a.href = url;
    a.download = 'data.csv';
    document.body.appendChild(a);
    a.click();
    };

  const handleFieldChange = (event) => {
    setField(event.target.value);
  };

  const handleRegexChange = (event) => {
    setRegex(event.target.value);
  };

  const handleSizeChange = (event) => {
    setSize(event.target.value);
  };

  const handlePositionChange = (event) => {
    setPosition(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    if (field && regex && size && position) {
      setIsSearching(true);
        const url = "http://127.0.0.1:8000/pandas/?field=" + field + "&regex=" + regex + "&size=" + size + "&position=" + position;
        fetch(url).then(
            response => response.json()).then(data => {
            downloadCsvfile(data['data']);
            setIsSearching(false);
        }
        ).catch(error => {
            alert(error);
            setIsSearching(false);
        }
        );
    }
  };

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        padding: '16px',
        maxWidth: '300px',
        margin: 'auto',
        marginTop: '100px',
      }}
    >
      <FormControl sx={{ marginBottom: '16px' }}>
        <InputLabel id="field-label">Field</InputLabel>
        <Select
          labelId="field-label"
          id="field-select"
          value={field}
          label="Field"
          onChange={handleFieldChange}
        >
        <MenuItem value="field1">Field 1</MenuItem>
        <MenuItem value="field2">Field 2</MenuItem>
        <MenuItem value="field3">Field 3</MenuItem>
        <MenuItem value="field4">Field 4</MenuItem>
        <MenuItem value="field5">Field 5</MenuItem>
        <MenuItem value="field6">Field 6</MenuItem>
        <MenuItem value="field7">Field 7</MenuItem>
        <MenuItem value="field8">Field 8</MenuItem>
        <MenuItem value="field9">Field 9</MenuItem>
        <MenuItem value="field10">Field 10</MenuItem>
        </Select>
      </FormControl>
      <TextField
        id="regex-input"
        label="Regex"
        variant="outlined"
        value={regex}
        onChange={handleRegexChange}
        sx={{ marginBottom: '16px' }}
      />
      <TextField
        id="size-input"
        label="Size"
        type="number"
        variant="outlined"
        value={size}
        onChange={handleSizeChange}
        sx={{ marginBottom: '16px' }}
      />
      <TextField
        id="position-input"
        label="Position"
        variant="outlined"
        value={position}
        onChange={handlePositionChange}
        sx={{ marginBottom: '16px' }}
      />
      <Button
        variant="contained"
        onClick={handleSubmit}
        disabled={isSearching || !field || !regex || !size || !position}
      >
        {isSearching ? (
          <CircularProgress sx={{ color: 'white' }} size={24} />
        ) : (
          'Search'
        )}
      </Button>
    </Box>
  );
};

export default Search;