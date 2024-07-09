import React from "react";
const Login = () => {
  const handleLogin = () => {
    window.location.href = "/login";
  };

  return (
    <div>
      <button onClick={handleLogin}>Login with GitHub</button>
    </div>
  );
};

export default Login;
