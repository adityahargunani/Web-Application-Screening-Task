import React, { useState } from "react";
import axios from "axios";

const API_BASE = "http://127.0.0.1:8000/api";

export default function Login({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async () => {
    try {
      const res = await axios.post(`${API_BASE}/login/`, {
        username,
        password,
      });
      onLogin(res.data.token);
    } catch {
      setError("Invalid credentials");
    }
  };

  return (
    <div style={{ padding: 40 }}>
      <h2>Login</h2>
      <input
        placeholder="Username"
        onChange={(e) => setUsername(e.target.value)}
      /><br /><br />
      <input
        type="password"
        placeholder="Password"
        onChange={(e) => setPassword(e.target.value)}
      /><br /><br />
      <button onClick={handleLogin}>Login</button>
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}
