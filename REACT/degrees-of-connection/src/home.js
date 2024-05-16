import React, { useState } from "react";

import api from "./api";
import filterResults from "./utils";

function Home() {
  const [username, setUsername] = useState("");
  const [results, setResults] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [noConnection, setNoConnection] = useState(false);

  // This function is triggered when the user clicks the "Submit" button
  const handleSubmit = () => {
    // Reset error state for a fresh attempt
    setError("");
    setLoading(true); // Set loading state to true when the request is in progress
    setResults([]); // Reset results state for a fresh attempt
    setNoConnection(false); // Reset noConnection state for a fresh attempt

    // Make an API request to the FastAPI backend
    api
      .post(`search/${username}`)
      .then((response) => {
        // Handle successful response, setting the data in `results`
        const filtered = filterResults(response.data);

        if (filtered.length === 0) {
          setNoConnection(true);
        } else {
          setResults(filtered);
        }
        setLoading(false);
      })
      .catch((err) => {
        // Log the error for debugging purposes
        console.error("Error fetching data:", err);
        setLoading(false);
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
  // Filter results to include only the last repository link for each user

  return (
    <div>
      <nav className="navbar navbar-expand-lg">
        <div className="search">
          <a className="navbar-brand" href="/">
            Seven Degrees of Torvalds
          </a>
        </div>
        <div id="github-icon">
          <a
            href="https://github.com/tobiadefami/seven-degrees-of-torvalds"
            target="_blank"
            rel="noopener noreferrer"
          >
            <svg
              width="43"
              height="44"
              viewBox="0 0 43 44"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M21.5 1.375C10.1162 1.375 0.895813 10.8098 0.895813 22.4583C0.895813 31.7877 6.79376 39.6676 14.9839 42.4611C16.0141 42.6456 16.4004 42.0131 16.4004 41.4597C16.4004 40.959 16.3747 39.2986 16.3747 37.5329C11.1979 38.508 9.85863 36.2416 9.44654 35.0556C9.21475 34.4495 8.21029 32.5783 7.33462 32.0776C6.61347 31.6823 5.58326 30.7072 7.30886 30.6808C8.93144 30.6545 10.0904 32.2094 10.4768 32.8419C12.3311 36.0307 15.293 35.1347 16.4777 34.5812C16.658 33.2108 17.1989 32.2884 17.7912 31.7614C13.2068 31.2343 8.41633 29.4158 8.41633 21.3515C8.41633 19.0586 9.21475 17.1611 10.5283 15.6853C10.3222 15.1582 9.60107 12.9972 10.7343 10.0982C10.7343 10.0982 12.4599 9.54479 16.4004 12.2593C18.0488 11.7849 19.8001 11.5477 21.5515 11.5477C23.3028 11.5477 25.0542 11.7849 26.7025 12.2593C30.6431 9.51844 32.3687 10.0982 32.3687 10.0982C33.5019 12.9972 32.7808 15.1582 32.5747 15.6853C33.8882 17.1611 34.6866 19.0323 34.6866 21.3515C34.6866 29.4422 29.8704 31.2343 25.286 31.7614C26.0329 32.4202 26.6768 33.6852 26.6768 35.6618C26.6768 38.4817 26.651 40.7481 26.651 41.4597C26.651 42.0131 27.0374 42.672 28.0676 42.4611C36.2062 39.6676 42.1041 31.7614 42.1041 22.4583C42.1041 10.8098 32.8838 1.375 21.5 1.375V1.375Z"
                fill="#111111"
              />
            </svg>
          </a>
        </div>
      </nav>

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
        {noConnection && <p>No connection found</p>}
        {loading && <div className="spinner"></div>}
        {results.map((item, index) => (
          <div key={index}>
            <div className="user">
              <a
                href={`https://github.com/${item[1]}`}
                target="_blank"
                rel="noopener noreferrer"
              >
                {item[1]}
              </a>
            </div>

            {item[0] ? (
              <div className="connections">
                <svg
                  width="30"
                  height="50"
                  viewBox="0 0 30 87"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M8.81548 71.3608C5.8343 67.7795 5.18888 62.4899 0.143458 58.8071C0.143458 61.1369 -0.215188 62.4851 0.20166 63.515C2.89093 70.1598 5.51431 76.8507 8.63536 83.2926C10.7078 87.5701 13.7209 88.1894 16.913 84.9253C21.0816 80.6631 24.8292 75.9414 28.3937 71.143C29.7588 69.3053 31.0976 66.7611 28.6002 63.8156C22.9125 66.3936 21.1836 72.883 16.1761 76.7287C16.0043 75.5304 15.7803 74.8292 15.8237 74.1452C16.7146 60.1273 15.7004 46.1888 14.3659 32.2429C13.5704 23.9297 13.3024 15.5665 12.6765 7.23514C12.5334 5.32979 12.1189 3.36584 11.3828 1.61966C11.0388 0.803894 9.66074 0.0843585 8.69415 0.00210268C8.04961 -0.0528559 6.88109 0.982371 6.68737 1.72559C6.20679 3.56797 5.85115 5.54237 5.97259 7.42941C6.82111 20.6119 7.8359 33.7834 8.7314 46.963C9.2786 55.0173 9.70843 63.0797 10.1911 71.1385C9.73253 71.2125 9.27402 71.2868 8.81548 71.3608Z"
                    fill="#F9C22E"
                  />
                </svg>
                <a
                  href={`https://github.com/${item[0]}`}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {item[0]}
                </a>
              </div>
            ) : null}
          </div>
        ))}
      </div>
    </div>
  );
}

export default Home;
