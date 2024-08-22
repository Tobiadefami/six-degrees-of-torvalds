import React from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";

const AboutPage = () => {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-4">How Degrees of Torvalds Works</h1>

      <section className="mb-6">
        <h2 className="text-2xl font-semibold mb-2">Purpose</h2>
        <p>
          Degrees of Torvalds finds the shortest connection path between any
          GitHub user and Linus Torvalds, the creator of Linux and Git, through
          shared repositories and collaborations.
        </p>
      </section>

      <section className="mb-6">
        <h2 className="text-2xl font-semibold mb-2">How It Works</h2>
        <ol className="list-decimal list-inside space-y-2">
          <li>Users log in securely using GitHub OAuth.</li>
          <li>Enter any GitHub username to search for connections.</li>
          <li>
            Our algorithm uses breadth-first search to find the shortest path to
            Linus Torvalds.
          </li>
          <li>
            The app displays the chain of connections, showing shared
            repositories along the way.
          </li>
        </ol>
      </section>

      <section className="mb-6">
        <h2 className="text-2xl font-semibold mb-2">Key Features</h2>
        <ul className="list-disc list-inside space-y-2">
          <li>
            Efficient path-finding algorithm to discover connections quickly
          </li>
          <li>
            Integration with GitHub API to fetch real-time collaboration data
          </li>
          <li>
            Advanced caching system for improved performance and reduced API
            calls
          </li>
          <li>
            Asynchronous operations for handling multiple searches concurrently
          </li>
          <li>
            Respect for GitHub API rate limits to ensure uninterrupted service
          </li>
        </ul>
      </section>

      <section className="mb-6">
        <h2 className="text-2xl font-semibold mb-2">Technology Stack</h2>
        <p>
          Built with Python (FastAPI) backend and React frontend, utilizing
          asyncio for efficient API requests and SQLite for caching. The app
          employs OAuth for secure authentication and adheres to GitHub's API
          guidelines.
        </p>
      </section>

      <section className="mb-6">
        <h2 className="text-2xl font-semibold mb-2">Privacy and Data Usage</h2>
        <p>
          We only access public GitHub data and do not store personal
          information beyond session requirements. Our caching system anonymizes
          and securely stores connection paths to optimize performance.
        </p>
      </section>

      <Link href="/">
        <Button>Back to Home</Button>
      </Link>
    </div>
  );
};

export default AboutPage;
