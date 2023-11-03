import { useCallback, useEffect, useState } from "react";
import { Status } from "./status";

export const useGetClient = (url) => {
  const [status, setStatus] = useState(Status.NotStarted);
  const [responseData, setResponseData] = useState();

  const fetchData = useCallback(async () => {
    setStatus(Status.Pending);

    const response = await fetch(`http://127.0.0.1:8000${url}`);

    if (response.status === 200) {
      setStatus(Status.Success);
      const jsonResponse = await response.json();
      setResponseData(jsonResponse);
      return;
    }
    setStatus(Status.Error);
  }, [url]);

  // useEffect(() => {
  //   fetchData();
  // }, [fetchData]);

  return {
    responseData: responseData,
    reload: fetchData,
    status: status,
  };
};
