# Degrees of Linus Torvalds

![Degrees of Connection](assets/degrees_of_connection.png)

## Overview

This project aims to find a connection between a given GitHub user and Linus Torvalds using the breadth-first search algorithm. The current scope is limited to finding connections to Linus Torvalds, but future updates may allow searching for connections between any two users.

## Features

- **User Authentication**: Users can log in and log out using their GitHub accounts.
- **Connection Search**: Find the shortest path between a given user and Linus Torvalds.
- **Progress Indicator**: Displays the progress of the search operation.
- **Fun Facts**: Shows interesting facts about Linus Torvalds and Linux during the search.

## Running the Project

The entire project runs on Docker. Follow the steps below to start the server using Docker:

1. **Build and Run the Docker Image**:
   ```sh
   docker compose up --build
   ```
   
2. **Access the Application**:
   Open your web browser and navigate to `http://0.0.0.0:8080`.

## Future Enhancements

- Extend the search functionality to allow finding connections between any two users.
- Improve the user interface and add more visual indicators.


## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.




