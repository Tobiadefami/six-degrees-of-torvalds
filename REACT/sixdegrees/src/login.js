import React from "react";
const Login = () => {
  const handleLogin = () => {
    window.location.href = "http://" + process.env.BACKEND_HOST + "/login";
  };

  return (
    <div>
      <button onClick={handleLogin}>Login with GitHub</button>
    </div>
  );
};

export default Login;
