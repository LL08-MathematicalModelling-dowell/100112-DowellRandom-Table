import React, { useEffect, useState } from "react";
import { TextField, Select, MenuItem, Button, Box, CircularProgress } from "@mui/material";
import { Status } from "./status";
import CsvTable from "./csvTable";
import LoadingSpinner from "./Spinner";

const Search = () => {
  const [apiKey, setApiKey] = useState("");
  const [size, setSize] = useState("");
  const [valueCount, setValueCount] = useState({});
  const [selectedFilterMethod, setSelectedFilterMethod] = useState(FilteringMethods[0]);
  const [submitting, setSubmitting] = useState(false);
  const [downloading, setDownloading] = useState(false);
  const [nextLink, setNextLink] = useState(null);
  const [dataCsv, setDataCsv] = useState(null);

  const isOddOrEven = selectedFilterMethod.method === "odd" || selectedFilterMethod.method === "even";

  const isSubmitDisabled = !apiKey || !size || (isOddOrEven ? false : !valueCount) || submitting;
  

const jsonToCsv = (jsonData) => {
  let csv = "";

  jsonData.forEach(function (row) {
    let data = row.join(",");
    csv += data + "\n";
  });
  return csv;
};

const downloadCsvfile = (data) => {
  setDownloading(true);
  let csvData = jsonToCsv(data);
  let blob = new Blob([csvData], { type: "text/csv" });
  let url = window.URL.createObjectURL(blob);
  let a = document.createElement("a");
  a.href = url;
  a.download = "DoWell_RandomTable_Data.csv";
  document.body.appendChild(a);
  a.click();
  setDownloading(false);
};

  const handleSubmit = async () => {
    setSubmitting(true);
    const secondResponse = await callSecondEndpoint();
   
    if (!secondResponse.data) {
      clearFields();
      setSubmitting(false);
      
      let errorMessage = "";
    
      if (secondResponse.error) {
        if (typeof secondResponse.error === "object") {
          Object.entries(secondResponse.error).forEach(([key, value]) => {
            errorMessage += `\n${key}: ${value.join(", ")}`;
          });
        } else {
          errorMessage = secondResponse.error;
        }
      } 
      alert(errorMessage);
      return;
    }
    
    setDataCsv(secondResponse.data);
    if (secondResponse.next_data_link) {
      setNextLink(secondResponse.next_data_link);
    }
    setSubmitting(false);
  };

  const callSecondEndpoint = async () => {
    let url = `https://uxlivinglab200112.pythonanywhere.com/api/without_pagination/?size=${size}&filter_method=${selectedFilterMethod.method}&api_key=${apiKey}`;

    if (selectedFilterMethod.method !== "no_filtering" && selectedFilterMethod.inputs.length > 0) {
      for (let input of selectedFilterMethod.inputs) {
        url += `&${input}=${valueCount[input]}`;
      }
    }
    
    const response = await fetch(url);
    if (response.status == 500){
      alert("Unexpected error");
    }
    setSubmitting(false)
    return response.json();
  };

  const reloadNextData = async () => {
    const response = await fetch(nextLink);
    const data = await response.json();
    setDataCsv(data.data);
    if (!data.next_data_link) {
      setNextLink(data.next_data_link);
    }
  }

  const clearFields = () => {
    setApiKey("");
    setSize("");
    setValueCount("");
  };

  const handleDownloadCsv = () => {
    if (dataCsv) {
      downloadCsvfile(dataCsv);
    }
  };

  return (
    <>
      <Box
        sx={{
          display: "flex",
          flexDirection: "row",
          gap : 2,
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
          id="size-input"
          label="sample size"
          type="number"
          variant="outlined"
          value={size}
          onChange={(e) => setSize(e.target.value)}
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
            selectedFilterMethod.inputs.map((input, index) => (
              <TextField
                key={index}
                label={input}
                type="number"
                variant="outlined"
                value={valueCount[input] || ''}
                onChange={(e) => setValueCount({ ...valueCount, [input]: e.target.value })}
              />
            ))
          }


          <Button
            onClick={handleSubmit}
            variant="contained"
            disabled={isSubmitDisabled}
          >
            {submitting ? <CircularProgress size={24} color="inherit" /> : "Submit"}
          </Button>
      </Box>

      <Box>
        {submitting ? (
          <Box
            sx={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              height: '100%',
            }}
          >
            <LoadingSpinner />
          </Box>
        ) : (
          dataCsv && (
            <>
              <CsvTable data={dataCsv} />
              <Button
                sx={{
                  display: 'flex',
                  alignItems: 'end',
                  justifyContent: 'end',
                }}
                onClick={handleDownloadCsv}
                variant="contained"
                disabled={!dataCsv}
              >
                {downloading ? <CircularProgress size={24} color="inherit" /> : "Download CSV"}
              </Button>
            </>
          )
        )}
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
    inputs: ["mini", "maxi"],
  },

  {
    label: "Not in between",
    method: "not_between",
    inputs: ["mini", "maxi"],
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

  {
    label: "By One Digit",
    method: "one_digits",
    inputs: [],
  },

  {
    label: "By First and Last Digit",
    method: "first_and_last_digits",
    inputs: [],
  }
];

