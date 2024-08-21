"use client";
import api from "../app/api";
import queryString from "query-string";
import { useEffect, useState } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

interface Connection {
  from: string;
  via: string;
  to: string;
}

interface ComponentProps {
  appName: string;
  initialDarkMode: boolean;
  currentYear: number;
  defaultUsername: string;
  connections: Connection[];
  user: any;
  username: any;
  onLogin: () => void;
  onLogout: () => void;
}

export function GitHubConnections({
  appName,
  initialDarkMode,
  currentYear,
  defaultUsername,
  connections,
  onLogin,
  onLogout,
  user,
  username,
}: ComponentProps) {
  const [isDarkMode, setIsDarkMode] = useState(initialDarkMode);
  const toggleDarkMode = () => {
    setIsDarkMode((prevState) => !prevState);
  };

  // const handleLogin = () => {
  //   const loginUrl = "/api/login";
  //   window.location.href = loginUrl;
  // };

  return (
    <div className={`flex flex-col min-h-screen ${isDarkMode ? "dark" : ""}`}>
      <header className="bg-background border-b shadow-sm sticky top-0 z-20">
        <div className="container flex items-center justify-between h-16 px-4 md:px-6">
          <Link
            href="#"
            className="flex items-center gap-2 text-lg font-semibold"
            prefetch={false}
          >
            <GithubIcon className="w-6 h-6" />
            <span>{appName}</span>
          </Link>
          <div className="flex items-center gap-4">
            <Button
              variant="outline"
              className="hidden md:inline-flex"
              onClick={toggleDarkMode}
            >
              {isDarkMode ? "Light Mode" : "Dark Mode"}
            </Button>
            {user ? (
              <Button
                variant="outline"
                className="hidden md:inline-flex"
                onClick={onLogout}
              >
                Logout
              </Button>
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
      <main className="flex-1 container px-4 py-8 md:px-6 md:py-12">
        <div className="max-w-xl mx-auto space-y-8">
          <div className="text-center space-y-2">
            <h1 className="text-3xl font-bold">Explore GitHub Connections</h1>
            <p className="text-muted-foreground">
              Enter a GitHub username to see its connections.
            </p>
          </div>
          <form className="space-y-4">
            <div>
              <Label htmlFor="username">GitHub Username</Label>
              <Input
                id="username"
                type="text"
                placeholder={`e.g., ${defaultUsername}`}
                className="w-full"
              />
            </div>
            <Button type="submit" className="w-full">
              Explore Connections
            </Button>
          </form>
          <Card className="p-6 md:p-8">
            <CardHeader>
              <CardTitle>Connections for @{defaultUsername}</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid gap-6 sm:grid-cols-1">
                {connections.map((connection, index) => (
                  <div
                    key={index}
                    className="bg-background dark:bg-card dark:text-card-foreground rounded-lg p-4 flex flex-col gap-4"
                  >
                    <div className="flex flex-col sm:flex-row items-center gap-2">
                      <Link href="#" className="font-medium" prefetch={false}>
                        @{connection.from}
                      </Link>
                      <ArrowRightIcon className="w-4 h-4 text-muted-foreground dark:text-muted-foreground sm:mx-2" />
                      <Link
                        href="#"
                        className="text-muted-foreground dark:text-muted-foreground"
                        prefetch={false}
                      >
                        {connection.via}
                      </Link>
                      <ArrowRightIcon className="w-4 h-4 text-muted-foreground dark:text-muted-foreground sm:mx-2" />
                      <Link href="#" className="font-medium" prefetch={false}>
                        @{connection.to}
                      </Link>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </main>
      <footer className="bg-background dark:bg-card border-t">
        <div className="container flex items-center justify-between h-16 px-4 md:px-6">
          <div className="text-sm text-muted-foreground dark:text-muted-foreground">
            &copy; {currentYear} {appName}
          </div>
          <div className="flex items-center gap-4">
            <Link
              href="#"
              className="text-muted-foreground dark:text-muted-foreground hover:text-foreground dark:hover:text-card-foreground"
              prefetch={false}
            >
              About
            </Link>
            <Link
              href="#"
              className="text-muted-foreground dark:text-muted-foreground hover:text-foreground dark:hover:text-card-foreground"
              prefetch={false}
            >
              Contact
            </Link>
            <Link
              href="#"
              className="text-muted-foreground dark:text-muted-foreground hover:text-foreground dark:hover:text-card-foreground"
              prefetch={false}
            >
              Privacy
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
