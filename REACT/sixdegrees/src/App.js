import React, { useState } from "react";
import { Route, BrowserRouter as Router, Routes } from "react-router-dom";

import Home from "./home";

function App() {
  const [setUsername] = useState("");

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home onUsernameSubmit={setUsername} />} />
      </Routes>
    </Router>
  );
}

export default App;
