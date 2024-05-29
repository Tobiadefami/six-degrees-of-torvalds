import React from "react";

const Login = () => {
  const handleLogin = () => {
    window.location.href = "http://127.0.0.1:8000/login";
  };

  return (
    <div>
      <button onClick={handleLogin}>Login with GitHub</button>
    </div>
  );
};

export default Login;
