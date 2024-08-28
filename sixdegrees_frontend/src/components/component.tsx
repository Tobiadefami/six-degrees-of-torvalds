"use client";
import Image from "next/image";
import api from "../app/api";
import queryString from "query-string";
import { useEffect, useState } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Puritan } from "next/font/google";

interface ComponentProps {
  repoUrl: string;
  appName: string;
  currentYear: number;
  defaultUsername: string;
  connections: (string | null)[][];
  user: any;
  username: any;
  error: string;
  noResult: boolean;
  submittedUsername: string;
  setSubmittedUsername: (submittedUsername: string) => void;
  setNoResults: (noResults: boolean) => void;
  setError: (error: string) => void;
  setUsername: (username: string) => void;
  onLogin: () => void;
  onLogout: () => void;
  isLoading: boolean;
  showLoginPrompt: boolean;
  setShowLoginPrompt: (show: boolean) => void;
  onSubmit: (e: React.FormEvent<HTMLFormElement>) => void;
}

export function GitHubConnections({
  appName,
  currentYear,
  defaultUsername,
  connections,
  onLogin,
  onLogout,
  user,
  username,
  setUsername,
  error,
  setError,
  noResult,
  setNoResults,
  submittedUsername,
  setSubmittedUsername,
  isLoading,
  showLoginPrompt,
  setShowLoginPrompt,
  onSubmit,
  repoUrl,
}: ComponentProps) {
  const Loader: React.FC = () => {
    const [dots, setDots] = useState("");

    useEffect(() => {
      const interval = setInterval(() => {
        setDots((prev) => (prev.length >= 3 ? "" : prev + "."));
      }, 500);

      return () => clearInterval(interval);
    }, []);

    return (
      <div className="flex justify-center items-center p-4">
        <p className="text-xl font-semibold text-gray-600">Searching{dots}</p>
      </div>
    );
  };
  return (
    <div className={`flex flex-col min-h-screen`}>
      <header className="bg-background border-b shadow-sm sticky top-0 z-20">
        <div className="container mx-auto flex items-center justify-between h-16 px-4 md:px-6">
          <Link
            href="/"
            className="flex items-center gap-2 text-lg font-semibold"
            prefetch={false}
          >
            <GithubIcon className="w-6 h-6" />
            <span>{appName}</span>
          </Link>
          <div className="flex items-center gap-4">
            {user ? (
              <>
                <Button
                  variant="outline"
                  className="hidden md:inline-flex"
                  onClick={onLogout}
                >
                  Logout
                </Button>
              </>
            ) : (
              <Button
                variant="outline"
                className="hidden md:inline-flex"
                onClick={onLogin}
              >
                Login with GitHub
              </Button>
            )}
            <Button variant="ghost" size="icon" className="md:hidden">
              <MenuIcon className="w-6 h-6" />
              <span className="sr-only">Toggle menu</span>
            </Button>
          </div>
        </div>
      </header>
      <main className="flex-1 container mx-auto px-4 py-8 md:px-6 md:py-12">
        <div className="max-w-xl mx-auto space-y-8">
          <div className="text-center space-y-2">
            <h1 className="text-3xl font-bold">Explore GitHub Connections</h1>
            <p className="text-muted-foreground">
              Enter a GitHub username to see how many degrees they are away from
              Linus Torvalds.
            </p>
          </div>
          <form className="space-y-4" onSubmit={onSubmit}>
            <div>
              <Label htmlFor="username">GitHub Username</Label>
              <Input
                id="username"
                type="text"
                placeholder={`e.g., ${defaultUsername}`}
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full"
              />
            </div>
            <Button type="submit" className="w-full">
              Explore Connections
            </Button>
          </form>

          {showLoginPrompt ? (
            <Card className="p-6 md:p-8">
              <CardHeader>
                <CardTitle>Login Required</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="mb-4">
                  To use Degrees of Torvalds, you need to log in with your
                  GitHub account. This allows us to access public GitHub data
                  and find connections accurately.
                </p>
                <div className="flex justify-between">
                  <Button
                    onClick={() => setShowLoginPrompt(false)}
                    variant="outline"
                  >
                    Close
                  </Button>
                  <Button onClick={onLogin}>Login with GitHub</Button>
                </div>
              </CardContent>
            </Card>
          ) : (
            <Card className="p-6 md:p-8">
              <CardHeader>
                <CardTitle>
                  {isLoading
                    ? `Finding connections for @${submittedUsername}`
                    : `Connections for @${submittedUsername}`}
                </CardTitle>
              </CardHeader>
              <CardContent className="flex justify-center p-0">
                {isLoading ? (
                  <Loader />
                ) : noResult ? (
                  <div className="flex flex-col items-center text-center">
                    <div className="relative w-[300px] h-[300px] mb-4">
                      <Image
                        src="/test.png"
                        alt="No connections found"
                        width={300}
                        height={300}
                      />
                    </div>
                    <p className="text-muted-foreground">
                      No connections found for{" "}
                      <Link
                        href={`https://github.com/${submittedUsername}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-500 hover:underline"
                      >
                        @{submittedUsername}
                      </Link>
                      .
                    </p>
                  </div>
                ) : connections.length > 0 ? (
                  <div className="grid gap-6 sm:grid-cols-1">
                    {connections.slice(0, -1).map((connection, index) => (
                      <div
                        key={index}
                        className="bg-background dark:bg-card dark:text-card-foreground rounded-lg p-4 flex flex-col gap-4"
                      >
                        <div className="flex flex-col sm:flex-row items-center gap-2">
                          <Link
                            href={`https://github.com/${connection[1]}`}
                            className="font-medium"
                            prefetch={false}
                            target="_blank"
                            rel="noopener noreferrer"
                          >
                            @{connection[1]}
                          </Link>
                          <ArrowRightIcon className="w-4 h-4 text-muted-foreground dark:text-muted-foreground sm:max-2xl:" />
                          <Link
                            href={`https://github.com/${connections[index + 1][0]}`}
                            className="text-muted-foreground dark:text-muted-foreground"
                            prefetch={false}
                            target="_blank"
                            rel="noopener noreferrer"
                          >
                            {connections[index + 1][0]?.split("/").pop()}
                          </Link>
                          <ArrowRightIcon className="w-4 h-4 text-muted-foreground dark:text-muted-foreground sm:max-2xl:" />
                          <Link
                            href={`https://github.com/${connections[index + 1][1]}`}
                            className="font-medium"
                            prefetch={false}
                            target="_blank"
                            rel="noopener noreferrer"
                          >
                            @{connections[index + 1][1]}
                          </Link>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : null}
              </CardContent>
            </Card>
          )}
        </div>
      </main>
      <footer className="bg-background dark:bg-card border-t">
        <div className="container mx-auto flex items-center justify-between h-16 px-4 md:px-6">
          <div className="text-sm text-muted-foreground dark:text-muted-foreground">
            &copy; {currentYear} {appName}
          </div>
          <div className="flex items-center gap-4">
            <Link
              href="/about"
              className="text-muted-foreground dark:text-muted-foreground hover:text-foreground dark:hover:text-card-foreground"
              prefetch={false}
            >
              How it Works
            </Link>
            <Link
              href={repoUrl}
              className="text-muted-foreground dark:text-muted-foreground hover:text-foreground dark:hover:text-card-foreground"
              target="_blank"
              rel="noopener noreferrer"
            >
              GitHub
            </Link>
          </div>
        </div>
      </footer>
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
