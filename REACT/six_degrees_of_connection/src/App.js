import React, { useState } from "react";
import { Route, BrowserRouter as Router, Routes } from "react-router-dom";

import Home from "./home";
import Login from "./login";

function App() {
  const [setUsername] = useState("");

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home onUsernameSubmit={setUsername} />} />
        <Route path="/" Component={<Login />} />
        <Route path="/home" element={<Home />} />
      </Routes>
    </Router>
  );
}

export default App;
