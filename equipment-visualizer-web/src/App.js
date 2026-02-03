import React, { useEffect, useState } from "react";
import Auth from "./Auth";
import Dashboard from "./Dashboard";
import Navbar from "./Navbar";
import { Toaster } from "react-hot-toast";

<Toaster position="top-right" />



export default function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [dark, setDark] = useState(
    localStorage.getItem("dark") === "true"
  );

  useEffect(() => {
    document.body.className = dark ? "dark" : "";
    localStorage.setItem("dark", dark);
  }, [dark]);

  const handleAuth = (t) => {
    localStorage.setItem("token", t);
    setToken(t);
  };

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    setToken(null);
  };


  if (!token) return <Auth onAuth={handleAuth} />;

  return (
    <>
      <Navbar
        onLogout={logout}
        dark={dark}
        toggleDark={() => setDark(!dark)}
      />
      <Dashboard
        token={token}
        username={localStorage.getItem("username")}
      />

    </>
  );
}
