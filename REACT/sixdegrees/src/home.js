import React, { useEffect, useState } from "react";

import api from "./api";
import arrow from "./arrow.svg";
import filterResults from "./utils";
import githubIcon from "./github-icon.svg";
import queryString from "query-string";

function Home() {
  const [username, setUsername] = useState("");
  const [results, setResults] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [noConnection, setNoConnection] = useState(false);
  const [user, setUser] = useState(null);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await api.get("user");
        setUser(response.data);
      } catch (error) {
        console.error("Error fetching user:", error);
      }
    };
    fetchUser();

    const { code } = queryString.parse(window.location.search);
    if (code) {
      fetchAccessToken(code);
    }
  }, []);

  const fetchAccessToken = async (code) => {
    try {
      const response = await api.get(`callback?code=${code}`);

      setUser(response.data.user);
      window.history.pushState({}, document.title, "/");
    } catch (error) {
      console.error("Error fetching access token:", error);
    }
  };

  const handleLogin = () => {
    const loginUrl = "/api/login";
    window.location.href = loginUrl;
  };

  const handleLogout = async () => {
    try {
      await api.get("/logout");
      setUser(null);
      window.location.href = "/";
    } catch (error) {
      console.error("Error logging out:", error);
    }
  };
  // This function is triggered when the user clicks the "Submit" button
  const handleSubmit = () => {
    if (!user) {
      handleLogin();
      return;
    }
    // Reset error state for a fresh attempt
    setError("");
    setLoading(true); // Set loading state to true when the request is in progress
    setResults([]); // Reset results state for a fresh attempt
    setNoConnection(false); // Reset noConnection state for a fresh attempt

    // Make an API request to the FastAPI backend
    api
      .post(`/search/${username}`)
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
            6° of Torvalds
          </a>
        </div>
        <div id="github-icon">
          <a
            href="https://github.com/tobiadefami/six-degrees-of-torvalds"
            target="_blank"
            rel="noopener noreferrer"
          >
            <img src={githubIcon} alt="github_icon" />
          </a>
        </div>
        <div className="login-button">
          {user ? (
            <>
              <span className="user-name">Welcome, {user.login}</span>
              <button onClick={handleLogout}>Logout</button>
            </>
          ) : (
            <button onClick={handleLogin}>Login with github</button>
          )}
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
