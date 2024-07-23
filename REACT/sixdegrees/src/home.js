import "./index.css";

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
  const [progress, setProgress] = useState(0);
  const [message, setMessage] = useState("");
  const [noConnection, setNoConnection] = useState(false);
  const [user, setUser] = useState(null);

  const messages = [
    "Did you know? Linus Torvalds created Git.",
    "Fun fact: The Linux kernel was first released in 1991.",
    "Trivia: Linus Torvalds named the Linux kernel after himself.",
    "Interesting: Git was originally developed to manage the Linux kernel.",
    "Did you know? Linux powers most of the world's supercomputers.",
  ];

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await api.get("user");
        setUser(response.data);
        // setUsername(response.data.login);
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

  const handleSubmit = () => {
    if (!user) {
      handleLogin();
      return;
    }
    setError("");
    setLoading(true);
    setResults([]);
    setNoConnection(false);
    setProgress(0);
    setMessage(messages[0]);

    const tickInterval = 2000;
    const estimatedTime = 10000; // Estimated time in milliseconds (e.g., 10 seconds)

    const interval = setInterval(() => {
      setProgress((prevProgress) => {
        const nextProgress =
          prevProgress + (tickInterval / estimatedTime) * 100;
        return nextProgress >= 100 ? 100 : nextProgress;
      });
      setMessage(messages[Math.floor(Math.random() * messages.length)]);
    }, tickInterval);

    api
      .post(`/search/${username}`)
      .then((response) => {
        clearInterval(interval);
        const filtered = filterResults(response.data);
        if (filtered.length === 0) {
          setNoConnection(true);
        } else {
          setResults(filtered);
        }
        setLoading(false);
        setProgress(100); // Ensure progress is set to 100% when the response is received
      })
      .catch((err) => {
        clearInterval(interval);
        console.error("Error fetching data:", err);
        setLoading(false);
        if (err.response) {
          setError(
            `Error: ${err.response.status} - ${err.response.data.detail}`
          );
        } else if (err.request) {
          setError(
            "No response received. Check if the backend server is running."
          );
        } else {
          setError(`Request error: ${err.message}`);
        }
        setProgress(0);
      });
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      handleSubmit();
    }
  };

  useEffect(() => {
    console.log(progress);
  }, [progress]);

  return (
    <div>
      <nav className="navbar navbar-expand-lg navbar-light bg-light">
        <div className="container-fluid">
          <a
            className="navbar-brand"
            href="https://github.com/tobiadefami/six-degrees-of-torvalds"
            target="_blank"
            rel="noopener noreferrer"
          >
            <img src={githubIcon} alt="github_icon" className="github-icon" />
          </a>
          <div className="mx-auto">
            <a className="navbar-brand" href="/">
              Degrees of Torvalds
            </a>
          </div>
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarNav"
            aria-controls="navbarNav"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarNav">
            <div className="ms-auto d-flex">
              {user ? (
                <>
                  <span className="navbar-text me-2">
                    Welcome, {user.login}
                  </span>
                  <button
                    className="btn btn-outline-danger"
                    onClick={handleLogout}
                  >
                    Logout
                  </button>
                </>
              ) : (
                <button
                  className="btn btn-outline-primary"
                  onClick={handleLogin}
                >
                  Login
                </button>
              )}
            </div>
          </div>
        </div>
      </nav>

      <div className="row">
        <input
          id="username"
          type="text"
          placeholder={user ? "Enter your username" : "Sign in to search"}
          value={username}
          disabled={!user}
          onChange={(e) => setUsername(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        <button id="submit" onClick={handleSubmit} disabled={!user}>
          Submit
        </button>
      </div>

      {error && <p>{error}</p>}

      <div id="result">
        {noConnection && <p>No connection found</p>}
        {results && results.length > 0 && (
          <div>
            You are {results.length - 1} degrees away from Linus Torvalds.
          </div>
        )}
        {loading && (
          <>
            <div className="progress-container">
              <div
                className="progress-bar"
                style={{ width: `${progress}%` }}
              ></div>
            </div>
            <div className="progress-message">{message}</div>
          </>
        )}
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
