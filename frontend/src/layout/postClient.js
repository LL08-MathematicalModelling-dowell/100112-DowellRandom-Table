import { useState } from "react";
import { Status } from "./status";

export const usePostClient = () => {
  const [status, setStatus] = useState(Status.NotStarted);
  const [responseData, setResponseData] = useState();

  return {
    status: status,
    responseData: responseData,
    postData: async (data, url) => {
      setResponseData(undefined);
      setStatus(Status.Pending);

      const response = await fetch(url, {
        method: "post",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (response.status === 201 || response.status === 200) {
        setStatus(Status.Success);
        const jsonResponse = await response.json();
        setResponseData(jsonResponse);
        return;
      }
      setStatus(Status.Error);
    },
  };
};

export const usePutClient = () => {
  const [status, setStatus] = useState(Status.NotStarted);
  const [responseData, setResponseData] = useState();

  return {
    status: status,
    responseData: responseData,
    postData: async (data, url) => {
      setResponseData(undefined);
      setStatus(Status.Pending);

      const response = await fetch(url, {
        method: "put",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (response.status === 201 || response.status === 200) {
        setStatus(Status.Success);
        const jsonResponse = await response.json();
        setResponseData(jsonResponse);
        return;
      }
      setStatus(Status.Error);
    },
  };
};
