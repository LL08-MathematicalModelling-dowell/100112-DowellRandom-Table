import React, { useEffect, useState } from "react";
import {
  TextField,
  Select,
  MenuItem,
  InputLabel,
  FormControl,
  Box,
  Button,
  CircularProgress,
  Typography,
} from "@mui/material";

import { useGetClient } from "./getClient";
import { Status } from "./status";

const filterValuesParams = (searchValues) => {
  const urlPart = searchValues.map((value) => {
    return `&${value.label}=${value.value}`;
  });

  return urlPart.join("");
};

const Search = () => {
  const [searchValues, setSearchValues] = useState(
    FilteringMethods[0].inputs.map((v) => {
      return { label: v, value: "" };
    })
  );

  const [size, setSize] = useState("");
  const [randomTableSize, setRandomTableSize] = useState("");

  const [selectedFilterMethod, setSelectedFilterMethod] = useState(
    FilteringMethods[0]
  );

  const { status, responseData, reload } = useGetClient(
    `/api?set_size=${randomTableSize}&size=${size}&filter_method=${
      selectedFilterMethod.method
    }${filterValuesParams(searchValues)}`
  );

  const submitRandomTableRequest = () => {
    console.log(size, selectedFilterMethod.method, searchValues);
    reload();
  };

  useEffect(() => {
    if (status == Status.Success && responseData !== undefined) {
      downloadCsvfile(responseData["data"]);
    }
  }, [status, responseData]);

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

        <Select
          value={selectedFilterMethod}
          label="Filtering option"
          onChange={(e) => {
            setSelectedFilterMethod(e.target.value);
            const sv = e.target.value.inputs.map((v) => {
              return { label: v, value: "" };
            });

            setSearchValues(sv);
          }}
          renderValue={(val) => val.label}
        >
          {FilteringMethods.map((value, index) => (
            <MenuItem value={value} key={index}>
              {value.label}
            </MenuItem>
          ))}
        </Select>

        {searchValues.map((value, index) => {
          return (
            <TextField
              placeholder={value.label}
              key={index}
              value={value.value}
              onChange={(e) => {
                const tempSearchValues = [...searchValues];
                tempSearchValues[index] = {
                  label: value.label,
                  value: e.target.value,
                };
                setSearchValues(tempSearchValues);
              }}
            />
          );
        })}

        <Button variant="contained" onClick={submitRandomTableRequest}>
          {status === Status.Pending ? "loading..." : "Submit"}
        </Button>
      </Box>
      <Typography>{responseData?.next_data_link}</Typography>
    </>
  );
};

export default Search;

const FilteringMethods = [
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
    label: "Exact",
    method: "exact",
    inputs: ["value"],
  },

  {
    label: "In between",
    method: "in_between",
    inputs: ["minimum", "maximum"],
  },

  {
    label: "not in between",
    method: "not_in_between",
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
