import React, { useState } from "react";

export default function Navbar({ onLogout, dark, toggleDark }) {
  const [open, setOpen] = useState(false);

  return (
    <div style={styles.nav}>
      <h2 style={styles.logo}>
         Chemical Equipment Parameter Visualizer
      </h2>

      <div style={styles.right}>
        <button className="secondary" onClick={toggleDark}>
          {dark ? " Light" : " Dark"}
        </button>

        <div style={styles.avatar} onClick={() => setOpen(!open)}>
          👤
        </div>

        {open && (
          <div style={styles.dropdown}>
            <p>Welcome User!</p>
            <p></p>
            <hr />
            <p align="centre" onClick={onLogout}> Logout</p>
          </div>
        )}
      </div>
    </div>
  );
}

const styles = {
  nav: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "16px 32px",
    background: "var(--card)",
    boxShadow: "0 4px 12px rgba(0,0,0,0.05)",
  },
  logo: {
    margin: 0,
    color: "var(--primary)",
  },
  right: {
    display: "flex",
    alignItems: "center",
    gap: 16,
  },
  avatar: {
    fontSize: 24,
    cursor: "pointer",
  },
  dropdown: {
    position: "absolute",
    right: 32,
    top: 70,
    background: "var(--card)",
    padding: 12,
    borderRadius: 8,
    boxShadow: "0 6px 16px rgba(0,0,0,0.2)",
  },
};
