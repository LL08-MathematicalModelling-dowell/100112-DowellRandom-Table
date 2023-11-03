import React, { useState } from "react";
import Navbar from "./layout/Navbar";
import Search from "./layout/Search";
import { Box } from "@mui/material";

function App() {
  const [searches, setSearches] = useState([]);

  const handleAddSearch = () => {
    setSearches([...searches, <Search key={searches.length} />]);
  };

  return (
    <>
      <Navbar onAddSearch={handleAddSearch} />

      <Search />
    </>
  );
}
export default App;
