import React, { useEffect, useRef, useState } from "react";
import axios from "axios";
import { motion } from "framer-motion";
import { FiUser, FiLock } from "react-icons/fi";

const API = "http://127.0.0.1:8000/api";

export default function Auth({ onAuth }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [remember, setRemember] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const userRef = useRef(null);
  const passRef = useRef(null);

  /* ---------- AUTO FOCUS ---------- */
  useEffect(() => {
    userRef.current.focus();
  }, []);

  /* ---------- REMEMBER ME ---------- */
  useEffect(() => {
    const savedUser = localStorage.getItem("remember_user");
    if (savedUser) {
      setUsername(savedUser);
      setRemember(true);
    }
  }, []);

  const handleSuccess = (token) => {
    if (remember) {
      localStorage.setItem("remember_user", username);
    } else {
      localStorage.removeItem("remember_user");
    }
    onAuth(token);
  };

  const login = async () => {
    try {
      setLoading(true);
      const res = await axios.post(`${API}/login/`, {
        username,
        password,
      });
      handleSuccess(res.data.token);
    } catch {
      setError("Invalid username or password");
    } finally {
      setLoading(false);
    }
  };

  const signup = async () => {
    try {
      setLoading(true);
      const res = await axios.post(`${API}/register/`, {
        username,
        password,
      });
      handleSuccess(res.data.token);
    } catch {
      setError("User already exists or invalid input");
    } finally {
      setLoading(false);
    }
  };

  /* ---------- ENTER KEY SUPPORT ---------- */
  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      login();
    }
  };

  return (
    <div style={styles.page}>
      {/* ---------- SUBTLE BACKGROUND SHAPES ---------- */}
      <div style={styles.blob1} />
      <div style={styles.blob2} />

      {/* ---------- LEFT INFO ---------- */}
      <motion.div
        style={styles.left}
        initial={{ opacity: 0, x: -40 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.6 }}
      >
        <h1 style={styles.title}>
          ⚙️ Chemical Equipment <br /> Parameter Visualizer
        </h1>

        <p style={styles.subtitle}>
          Analyze chemical equipment data using interactive charts,
          per-user history, and exportable reports.
        </p>

        <ul style={styles.list}>
          <li>📊 Interactive analytics</li>
          <li>📁 Secure dataset history</li>
          <li>📄 PDF & image exports</li>
          <li>🔐 Token-based authentication</li>
        </ul>
      </motion.div>

      {/* ---------- AUTH CARD ---------- */}
      <motion.div
        style={styles.right}
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
      >
        <div className="card" style={styles.card}>
          <h2>Welcome 👋</h2>
          <p style={{ opacity: 0.7 }}>
            Login or create an account to continue
          </p>

          <div style={styles.inputGroup}>
            <FiUser />
            <input
              ref={userRef}
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              onKeyDown={handleKeyDown}
            />
          </div>

          <div style={styles.inputGroup}>
            <FiLock />
            <input
              ref={passRef}
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              onKeyDown={handleKeyDown}
            />
          </div>

          <label style={styles.remember}>
            <input
              type="checkbox"
              checked={remember}
              onChange={() => setRemember(!remember)}
            />
            Remember me
          </label>

          {error && (
            <p style={{ color: "#ef4444", fontSize: 14 }}>{error}</p>
          )}

          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.97 }}
            onClick={login}
            disabled={loading}
          >
            {loading ? "Logging in..." : "Login"}
          </motion.button>

          <motion.button
            className="secondary"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.97 }}
            onClick={signup}
            disabled={loading}
            style={{ marginTop: 10 }}
          >
            Sign Up
          </motion.button>
        </div>
      </motion.div>
    </div>
  );
}

/* ---------- STYLES ---------- */
const styles = {
  page: {
    minHeight: "100vh",
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    padding: "40px",
    position: "relative",
    overflow: "hidden",
  },

  blob1: {
    position: "absolute",
    width: 400,
    height: 400,
    background: "#93c5fd",
    borderRadius: "50%",
    top: "-100px",
    left: "-100px",
    opacity: 0.25,
    filter: "blur(80px)",
  },

  blob2: {
    position: "absolute",
    width: 350,
    height: 350,
    background: "#38bdf8",
    borderRadius: "50%",
    bottom: "-100px",
    right: "-100px",
    opacity: 0.25,
    filter: "blur(80px)",
  },

  left: {
    flex: 1,
    padding: "40px",
    zIndex: 1,
  },

  right: {
    flex: 1,
    display: "flex",
    justifyContent: "center",
    zIndex: 1,
  },

  title: {
    fontSize: 42,
    color: "var(--primary)",
    marginBottom: 20,
  },

  subtitle: {
    fontSize: 18,
    maxWidth: 480,
    opacity: 0.8,
    marginBottom: 30,
  },

  list: {
    listStyle: "none",
    padding: 0,
    fontSize: 16,
    lineHeight: "2rem",
  },

  card: {
    width: 380,
  },

  inputGroup: {
    display: "flex",
    alignItems: "center",
    gap: 10,
    marginBottom: 14,
  },

  remember: {
    display: "flex",
    alignItems: "center",
    gap: 6,
    marginBottom: 12,
    fontSize: 14,
  },
};
