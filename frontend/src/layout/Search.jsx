import React, { useEffect, useState } from "react";
import { TextField, Select, MenuItem, Button, Box } from "@mui/material";
import { Status } from "./status";
import CsvTable from "./csvTable";

const Search = () => {
  const [apiKey, setApiKey] = useState("");
  const [randomTableSize, setRandomTableSize] = useState("");
  const [size, setSize] = useState("");
  const [position, setPosition] = useState("");
  const [valueCount, setValueCount] = useState("");
  const [selectedFilterMethod, setSelectedFilterMethod] = useState(FilteringMethods[0]);
  const [submitting, setSubmitting] = useState(false);
  const [nextLink, setNextLink] = useState(null);
  const [dataCsv, setDataCsv] = useState(null);

  const isSubmitDisabled = !apiKey || !randomTableSize || !size || !position || !valueCount || submitting;

  const handleSubmit = async () => {
    setSubmitting(true);
    const firstResponse = await callFirstEndpoint();
    if (firstResponse.success == false) {
      clearFields();
      setSubmitting(false);
      alert(`${firstResponse.message}`);
      return;
    }
    const secondResponse = await callSecondEndpoint();
   
    if (!secondResponse.data) {
      clearFields();
      setSubmitting(false);
      
      let errorMessage = "";
    
      if (secondResponse.error) {
        // Check if secondResponse.error is an object
        if (typeof secondResponse.error === "object") {
          // Iterate over the keys and values of the error object
          Object.entries(secondResponse.error).forEach(([key, value]) => {
            // Concatenate each key and its corresponding error messages
            errorMessage += `\n${key}: ${value.join(", ")}`;
          });
        } else {
          // If secondResponse.error is not an object, use it directly
          errorMessage = secondResponse.error;
        }
      }
    
      // Show the error message in the alert
      alert(errorMessage);
      return;
    }
    
    setDataCsv(secondResponse.data);
    downloadCsvfile(secondResponse.data);
    if (secondResponse.next_data_link) {
      setNextLink(secondResponse.next_data_link);
    }
    setSubmitting(false);
  };

  const callSecondEndpoint = async () => {
    const response = await fetch(`http://uxlivinglab200112.pythonanywhere.com/api?set_size=${randomTableSize}&size=${size}&filter_method=${selectedFilterMethod.method}&value=${valueCount}&api_key=${apiKey}&position=${position}`);
    return response.json();
  };

  const callFirstEndpoint= async () => {
    const url = `https://100105.pythonanywhere.com/api/v3/process-services/?type=api_service&api_key=${apiKey}`;
    const payload = {
        service_id: "DOWELL10048"
    };

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        return await response.json();
    } catch (error) {
        console.error("Error:", error);
        throw error;
    }
  };

  const reloadNextData = async () => {
    const response = await fetch(nextLink);
    const data = await response.json();
    setDataCsv(data.data);
    downloadCsvfile(data.data);
    if (!data.next_data_link) {
      setNextLink(data.next_data_link);
    }
  }

  const clearFields = () => {
    setApiKey("");
    setRandomTableSize("");
    setSize("");
    setPosition("");
    setValueCount("");
  };

  return (
    <>
      <Box
        sx={{
          display: "flex",
          flexDirection: "row",
          padding: "16px",
          marginTop: "100px",
          alignItems: "center",
        }}
      >
        <TextField
          label="api_key"
          type="text"
          variant="outlined"
          value={apiKey}
          onChange={(e) => setApiKey(e.target.value)}
        />
        <TextField
          label="random set size"
          type="number"
          variant="outlined"
          value={randomTableSize}
          onChange={(e) => setRandomTableSize(e.target.value)}
        />

        <TextField
          id="size-input"
          label="sample size"
          type="number"
          variant="outlined"
          value={size}
          onChange={(e) => setSize(e.target.value)}
        />
        <TextField
          id="size-input"
          label="Position of the page"
          type="number"
          variant="outlined"
          value={position}
          onChange={(e) => setPosition(e.target.value)}
        />

        <Select
          value={selectedFilterMethod}
          label="Filtering option"
          onChange={(e) => {
            setSelectedFilterMethod(e.target.value);
            const sv = e.target.value.inputs.map((v) => {
              return { label: v, value: "" };
            });
          }}
          renderValue={(val) => val.label}
        >
          {FilteringMethods.map((value, index) => (
            <MenuItem value={value} key={index}>
              {value.label}
            </MenuItem>
          ))}
        </Select>

        {
          selectedFilterMethod !==  FilteringMethods[0] && <TextField
          label="value"
          type="number"
          variant="outlined"
          value={valueCount}
          onChange={(e) => setValueCount(e.target.value)}
        />
        }

       
      </Box>
      {nextLink && (
        <Button
          onClick={reloadNextData}
          variant="contained"
        >
          Next Data
        </Button>
      )}

      <Button
        onClick={handleSubmit}
        variant="contained"
        disabled={isSubmitDisabled}
      >
        {submitting ? "Loading..." : "Submit"}
      </Button>

      <Box>
        {dataCsv && <CsvTable data={dataCsv} />}
      </Box>
    </>
  );
};

export default Search;

const FilteringMethods = [
  {
    label: "No filtering",
    method: "no_filtering",
    inputs: [],
  },
  { label: "Regex", method: "regex", inputs: ["value"] },

  {
    label: "Contains",
    method: "contains",
    inputs: ["value"],
  },

  {
    label: "Not contains",
    method: "not_contains",
    inputs: ["value"],
  },

  {
    label: "Starts with",
    method: "starts_with",
    inputs: ["value"],
  },

  {
    label: "Ends with",
    method: "ends_with",
    inputs: ["value"],
  },

  {
    label: "In between",
    method: "between",
    inputs: ["minimum", "maximum"],
  },

  {
    label: "Not in between",
    method: "not_between",
    inputs: ["minimum", "maximum"],
  },
  {
    label: "Greater than",
    method: "greater_than",
    inputs: ["value"],
  },
  {
    label: "Less than",
    method: "less_than",
    inputs: ["value"],
  },
  {
    label: "Odd",
    method: "odd",
    inputs: [],
  },
  {
    label: "Even",
    method: "even",
    inputs: [],
  },

  {
    label: "Multiple of",
    method: "multiple_of",
    inputs: ["value"],
  },
];

const jsonToCsv = (jsonData) => {
  let csv = "";

  jsonData.forEach(function (row) {
    let data = row.join(",");
    csv += data + "\n";
  });
  return csv;
};

const downloadCsvfile = (data) => {
  let csvData = jsonToCsv(data);
  let blob = new Blob([csvData], { type: "text/csv" });
  let url = window.URL.createObjectURL(blob);
  let a = document.createElement("a");
  a.href = url;
  a.download = "data.csv";
  document.body.appendChild(a);
  a.click();
};
