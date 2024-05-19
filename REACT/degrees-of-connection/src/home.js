import React, { useState } from "react";

import api from "./api";
import arrow from "./arrow.svg";
import filterResults from "./utils";
import githubIcon from "./github-icon.svg";

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
            <img src={githubIcon} alt="github_icon" />
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
          <React.Fragment key={index}>
            {item[0] ? (
              <div className="connections">
                <img src={arrow} alt="Arrow" />
                <a
                  href={`https://github.com/${item[0]}`}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {item[0]}
                </a>
              </div>
            ) : null}

            <div className="user">
              <a
                href={`https://github.com/${item[1]}`}
                target="_blank"
                rel="noopener noreferrer"
              >
                {item[1]}
              </a>
            </div>
          </React.Fragment>
        ))}
      </div>
    </div>
  );
}

export default Home;
