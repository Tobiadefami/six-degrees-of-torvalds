// six-degrees-of-torvalds/sixdegrees_frontend/src/app/page.tsx
"use client";
import { useCallback } from "react";
import React, { useEffect, useState } from "react";
import api from "./api";
import filterResults from "./FilterResults";
import queryString from "query-string";
import { GitHubConnections } from "@/components/component";
import { setTimeout, clearTimeout } from "timers";
interface User {
  login: string;
}

const DEFAULT_USERNAME = "octocat";
const repoUrl = "https://github.com/Tobiadefami/six-degrees-of-torvalds";

export default function Home() {
  const [user, setUser] = useState<User | null>(null);
  const [username, setUsername] = useState(DEFAULT_USERNAME);
  const [connections, setConnections] = useState([
    [null, "octocat"],
    ["gamify/switchboard", "gamify"],
    ["torvalds/linux", "torvalds"],
  ]);
  const [error, setError] = useState("");
  const [submittedUsername, setSubmittedUsername] = useState(DEFAULT_USERNAME);
  const [noResult, setNoResults] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [showLoginPrompt, setShowLoginPrompt] = useState(false);

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
    if (code && typeof code === "string") {
      fetchAccessToken(code);
    }
  }, []);

  useEffect(() => {
    if (user) {
      setUsername(user.login);
    } else {
      setUsername(DEFAULT_USERNAME);
    }
  }, [user]);

  const fetchAccessToken = async (code: string) => {
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
      setUsername(DEFAULT_USERNAME);
      window.location.href = "/";
    } catch (error) {
      console.error("Error logging out:", error);
    }
  };

  const handleSubmit = useCallback(
    (e: React.FormEvent<HTMLFormElement>) => {
      e.preventDefault();
      if (!user) {
        setShowLoginPrompt(true);
      } else {
        setNoResults(false);
        setIsLoading(true);
        const normalizedUsername = username.toLowerCase();
        setSubmittedUsername(normalizedUsername);
        console.log(normalizedUsername);
        api
          .post(`/search/${normalizedUsername}`)
          .then((response) => {
            const filtered = filterResults(response.data);
            if (filtered.length === 0) {
              setNoResults(true);
            } else {
              setConnections(filtered);
            }
          })
          .catch((err) => {
            console.error("Error fetching data:", err);
            if (err.response) {
              setError(
                `Error: ${err.response.status} - ${err.response.data.detail}`,
              );
            } else if (err.request) {
              setError(
                "No response received. Check if the backend server is running.",
              );
            } else {
              setError(`Request error: ${err.message}`);
            }
          })
          .finally(() => {
            setIsLoading(false);
          });
      }
    },
    [user, username],
  ); // Dependencies

  return (
    <div>
      <GitHubConnections
        repoUrl={repoUrl}
        appName="GitHub Connections"
        currentYear={2024}
        defaultUsername={DEFAULT_USERNAME}
        connections={connections}
        user={user}
        username={username}
        setUsername={setUsername}
        error={error}
        setError={setError}
        noResult={noResult}
        setNoResults={setNoResults}
        onLogin={handleLogin}
        onLogout={handleLogout}
        onSubmit={handleSubmit}
        submittedUsername={submittedUsername}
        setSubmittedUsername={setSubmittedUsername}
        isLoading={isLoading}
        showLoginPrompt={showLoginPrompt}
        setShowLoginPrompt={setShowLoginPrompt}
      />
    </div>
  );
}

function ArrowRightIcon(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M5 12h14" />
      <path d="m12 5 7 7-7 7" />
    </svg>
  );
}

function GithubIcon(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4" />
      <path d="M9 18c-4.51 2-5-2-7-2" />
    </svg>
  );
}

function MenuIcon(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <line x1="4" x2="20" y1="12" y2="12" />
      <line x1="4" x2="20" y1="6" y2="6" />
      <line x1="4" x2="20" y1="18" y2="18" />
    </svg>
  );
}
