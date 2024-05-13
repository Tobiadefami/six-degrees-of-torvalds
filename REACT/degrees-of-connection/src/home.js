import React, { useState } from "react";

import api from "./api"; // Adjust the path to where your axios instance is located

function Home() {
  const [username, setUsername] = useState("");
  const [results, setResults] = useState([]);
  const [error, setError] = useState("");

  // This function is triggered when the user clicks the "Submit" button
  const handleSubmit = () => {
    // Reset error state for a fresh attempt
    setError("");

    // Make an API request to the FastAPI backend
    api
      .post(`/search/${username}`)
      .then((response) => {
        // Handle successful response, setting the data in `results`
        setResults(response.data);
      })
      .catch((err) => {
        // Log the error for debugging purposes
        console.error("Error fetching data:", err);

        // Provide user-friendly feedback
        if (err.response) {
          // Server responded with a status outside the 2xx range
          setError(
            `Error: ${err.response.status} - ${err.response.data.detail}`
          );
        } else if (err.request) {
          // No response received from the server
          setError(
            "No response received. Check if the backend server is running."
          );
        } else {
          // Something went wrong while setting up the request
          setError(`Request error: ${err.message}`);
        }
      });
  };

  return (
    <div id="search">
      <h1 id="title">Six degrees of Torvalds</h1>
      <div className="row">
        <input
          id="username"
          type="text"
          placeholder="Enter your username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />

        <button id="submit" onClick={handleSubmit}>
          Submit
        </button>
      </div>
      {error && <p>{error}</p>}
      <div id="result">
        {results.map((item, index) => (
          <div key={index}>
            <div className="user">{item[1]}</div>

            {item[0] ? (
              <div className="connections">
                <svg
                  width="30"
                  height="87"
                  viewBox="0 0 30 87"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M8.81548 71.3608C5.8343 67.7795 5.18888 62.4899 0.143458 58.8071C0.143458 61.1369 -0.215188 62.4851 0.20166 63.515C2.89093 70.1598 5.51431 76.8507 8.63536 83.2926C10.7078 87.5701 13.7209 88.1894 16.913 84.9253C21.0816 80.6631 24.8292 75.9414 28.3937 71.143C29.7588 69.3053 31.0976 66.7611 28.6002 63.8156C22.9125 66.3936 21.1836 72.883 16.1761 76.7287C16.0043 75.5304 15.7803 74.8292 15.8237 74.1452C16.7146 60.1273 15.7004 46.1888 14.3659 32.2429C13.5704 23.9297 13.3024 15.5665 12.6765 7.23514C12.5334 5.32979 12.1189 3.36584 11.3828 1.61966C11.0388 0.803894 9.66074 0.0843585 8.69415 0.00210268C8.04961 -0.0528559 6.88109 0.982371 6.68737 1.72559C6.20679 3.56797 5.85115 5.54237 5.97259 7.42941C6.82111 20.6119 7.8359 33.7834 8.7314 46.963C9.2786 55.0173 9.70843 63.0797 10.1911 71.1385C9.73253 71.2125 9.27402 71.2868 8.81548 71.3608Z"
                    fill="#F9C22E"
                  />
                </svg>
                {item[0]}
              </div>
            ) : null}
          </div>
        ))}
      </div>
    </div>
  );
}

export default Home;
