# Degrees of Linus Torvalds
https://www.sixdegreesofgithub.com

<img src="./assets/degrees_of_connection.png"  width="300" height="300">

Explore GitHub connections like never before. Discover how you or any other GitHub user connects to Linus Torvalds through shared repositories.

![Degrees of Connection](./assets/degrees_of_connection.png)

## Introduction

**Degrees of Linus Torvalds** applies the ![Six Degrees of Kevin Bacon](https://oracleofbacon.org/) concept to GitHub users, using a breadth-first search (BFS) algorithm to map the shortest path of collaboration from any given GitHub user to Linus Torvalds via shared repositories.

## How Connections Are Formed

### Nodes and Edges

Each GitHub user is represented as a **node**. A **repository** serves as an **edge** that connects two users when both have contributed to it. This framework maps collaborative relationships on GitHub.

### Degrees of Connection

- **First Degree Connection**: Users who have directly contributed to the same repository.
- **Second Degree Connection**: Users connected through another user who shares repositories with both. The BFS algorithm explores these connections to map pathways from a starting user to Linus Torvalds.

## Installation and Setup

### Prerequisites

- **Docker**: Ensure Docker is installed on your system, as it is required to containerize and run the services. This include docker-compose for handling the multi-container setup.

### GitHub OAuth Setup

For user authentication, a GitHub OAuth App is required:
1. Create an OAuth App in your GitHub account under 'Developer settings' > 'OAuth Apps'.
2. Use `http://0.0.0.0:8080` as the Homepage URL and `http://0.0.0.0:8080/api/app-login` as the Authorization callback URL.
3. Record your Client ID and Client Secret for environment setup.

### Environment Setup

Add these environment variables to your bashrc

```plaintext
GITHUB_APP_CLIENT_ID=<your_github_app_client_id>
GITHUB_APP_CLIENT_SECRET=<your_github_app_client_secret>
GITHUB_APP_ID=<your_github_app_id>
SIX_DEGREES_ENVIRONMENT=development # or production
SECRET_KEY=<your_secret_key>
NGINX_HOST=0.0.0.0:8080
```

### Running the Application

Run this code in your terminal

```bash
docker compose up --build
```
Access the application at http://0.0.0.0:8080


### Addressing User Authentication Concerns

While we understand the desire for simplicity, GitHub's API usage policies necessitate OAuth authentication to avoid rate limits and ensure user data privacy. Authenticating via GitHub allows us to access more detailed data without quickly exhausting API limits, thereby maintaining the application's performance and reliability. Rest assured, the auth step has read-only access to your commit history.

### Caching Strategy

To enhance performance and minimize API calls, we build a cache using a BFS algorithm up to six degrees starting from Linus Torvalds. This cache, stored in a SQLite database, gradually learns and stores paths, making the search for connections faster and less dependent on live API calls. Building this cache is an ongoing process and will enhance the user experience as it grows more comprehensive.

### Contributing
Contributions are welcome! To contribute, please fork the repository, make your changes, and submit a pull request.

### Future Enhancements

- Expanding Search Capability: Allow finding connections between any two GitHub users.
- UI Improvements: Enhance interface for better mobile usability.
