import React, { useEffect, useState } from "react";
import axios from "axios";
import { Pie, Bar } from "react-chartjs-2";
import { motion } from "framer-motion";

/* ---------- Chart.js registration ---------- */
import {
  Chart as ChartJS,
  ArcElement,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  ArcElement,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend
);

const API = "http://127.0.0.1:8000/api";

export default function Dashboard({ token, username }) {
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState(null);
  const [history, setHistory] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(false);
  const [fileInfo, setFileInfo] = useState(null);
  const [pdfUrl, setPdfUrl] = useState(null);
  const [selectedId, setSelectedId] = useState(null);

  const headers = { Authorization: `Token ${token}` };

  useEffect(() => {
    loadHistory();
  }, []);

  const loadSummaryFromHistory = async (datasetId) => {
    try {
      setLoading(true);

      const res = await axios.get(
        `${API}/summary/${datasetId}/`,
        { headers }
      );

      setSummary(res.data);
      setSelectedId(datasetId);
      setPdfUrl(null); // reset PDF preview
    } catch (err) {
      alert("Failed to load dataset summary");
    } finally {
      setLoading(false);
    }
  };


  const loadHistory = async () => {
    const res = await axios.get(`${API}/history/`, { headers });
    setHistory(res.data);
  };

  const uploadCSV = async () => {
    if (!file) return;
    setLoading(true);

    const fd = new FormData();
    fd.append("file", file);

    const res = await axios.post(`${API}/upload/`, fd, { headers });

    setSummary(res.data.summary);

    setFileInfo({
      name: file.name,
      size: (file.size / 1024).toFixed(2) + " KB",
      uploadedAt: new Date().toLocaleString(),
      id: res.data.id,
    });

    setPdfUrl(null);
    loadHistory();
    setLoading(false);
  };

  const downloadPDF = async () => {
    const res = await axios.get(
      `${API}/report/${fileInfo.id}/`,
      { headers, responseType: "blob" }
    );

    const url = URL.createObjectURL(res.data);
    setPdfUrl(url);

    const link = document.createElement("a");
    link.href = url;
    link.download = "analysis_report.pdf";
    link.click();
  };

  /* ---------- SUMMARY CARD ---------- */
  const StatCard = ({ title, value, unit, color }) => (
  <div
    className="card"
    style={{
      width: 220,
      textAlign: "center",
      borderTop: `4px solid ${color}`,
      overflow: "hidden",
    }}
  >
    <h4 style={{ marginBottom: 12 }}>{title}</h4>

    <div
      style={{
        fontSize: 28,
        fontWeight: 700,
        whiteSpace: "nowrap",
        overflow: "hidden",
        textOverflow: "ellipsis",
      }}
      title={`${value} ${unit}`}
    >
      {value}
    </div>

    <div style={{ fontSize: 14, opacity: 0.7, marginTop: 4 }}>
      {unit}
    </div>
  </div>
);


  /* ---------- FILTER HISTORY ---------- */
  const filteredHistory = history.filter((h) =>
    h.name.toLowerCase().includes(search.toLowerCase())
  );

  const getTypeDistributionWithPercent = () => {
    if (!summary) return [];

    const entries = Object.entries(summary.type_distribution);
    const total = entries.reduce((sum, [, count]) => sum + count, 0);

    return entries.map(([type, count]) => ({
      type,
      count,
      percentage: ((count / total) * 100).toFixed(1),
    }));
  };


  return (
    <div style={{ padding: 40 }}>
      <motion.div
        className="card"
        initial={{ opacity: 0, y: -15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        style={{
          marginBottom: 32,
          background: "linear-gradient(135deg, #2563eb, #38bdf8)",
          color: "white",
        }}
      >
        <h2 style={{ marginBottom: 8 }}>
           Welcome back {username}!
        </h2>
        <p style={{ opacity: 0.9 }}>
          Ready to analyze your chemical equipment data and generate insights?
        </p>
      </motion.div>


      {/* ================= WELCOME ================= */}
      <motion.div className="card" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
        <h2> Chemical Equipment Parameter Visualizer</h2>
        <p style={{ opacity: 0.7 }}>
          Upload datasets to analyze flowrate, pressure, and temperature
          using interactive visualizations and exportable reports.
        </p>
      </motion.div>

      {/* ================= UPLOAD ================= */}
      <motion.div className="card" style={{ marginTop: 32 }}>
        <h3> Upload Dataset</h3>
        <input
            type="file"
            accept=".csv"
            onChange={(e) => {
              const selectedFile = e.target.files[0];

              if (selectedFile && !selectedFile.name.endsWith(".csv")) {
                alert("Only CSV files are allowed");
                e.target.value = "";
                return;
              }

              setFile(selectedFile);
            }}
          />
        <br /><br />
        <button onClick={uploadCSV} disabled={loading}>
          {loading ? "Processing..." : "Analyze CSV"}
        </button>
      </motion.div>

      {/* ================= FILE INFO + PDF ================= */}
      {fileInfo && (
        <motion.div className="card" style={{ marginTop: 32 }}>
          <h3> File Information</h3>
          <ul>
            <li><b>Name:</b> {fileInfo.name}</li>
            <li><b>Size:</b> {fileInfo.size}</li>
            <li><b>Uploaded:</b> {fileInfo.uploadedAt}</li>
            <li><b>Total Records:</b> {summary.total_count}</li>
          </ul>

          <button onClick={downloadPDF}>
             Generate & Download PDF
          </button>
        </motion.div>
      )}

      {/* ================= SUMMARY TILES ================= */}
      {summary && (
        <motion.div
          style={{ display: "flex", gap: 24, marginTop: 32 }}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          <StatCard
            title="Average Flowrate"
            value={summary.statistics.flowrate.avg.toFixed(1)}
            unit="L/min"
            color="#22c55e"
          />

          <StatCard
            title="Average Pressure"
            value={summary.statistics.pressure.avg.toFixed(2)}
            unit="bar"
            color="#f97316"
          />

          <StatCard
            title="Average Temperature"
            value={summary.statistics.temperature.avg.toFixed(1)}
            unit="°C"
            color="#a855f7"
          />

        </motion.div>
      )}

      {/* ================= CHARTS ================= */}
      {summary && (
        <motion.div style={{ display: "flex", gap: 32, marginTop: 32 }}>
          <div
            className="card"
            style={{
              display: "flex",
              gap: 32,
              alignItems: "flex-start",
            }}
          >
            {/* ---------- PIE CHART ---------- */}
            <div style={{ width: 400 }}>
              <h4>Equipment Type Distribution</h4>

              <Pie
                data={{
                  labels: Object.keys(summary.type_distribution),
                  datasets: [
                    {
                      data: Object.values(summary.type_distribution),
                      backgroundColor: [
                        "#22c55e",
                        "#f97316",
                        "#a855f7",
                        "#ef4444",
                        "#14b8a6",
                        "#0037ff",
                        "#a11942",
                        "#e9de0d",
                        "#b8148c",
                        "#0dff00",
                        "#6c14b8",
                      ],
                    },
                  ],
                }}
                options={{
                  plugins: {
                    tooltip: {
                      callbacks: {
                        label: function (context) {
                          const data = context.dataset.data;
                          const total = data.reduce((a, b) => a + b, 0);
                          const value = context.parsed;
                          const percentage = ((value / total) * 100).toFixed(1);
                          return `${context.label}: ${value} (${percentage}%)`;
                        },
                      },
                    },
                    legend: {
                      position: "bottom",
                    },
                  },
                }}
              />

              <p style={{ fontSize: 13, opacity: 0.6, marginTop: 8 }}>
                Hover over chart segments to see exact percentage values.
              </p>
            </div>

            {/* ---------- PERCENTAGE TABLE ---------- */}
            <div style={{ minWidth: 300 }}>
              <h4>Distribution Summary</h4>

              <table style={{ width: "100%", borderCollapse: "collapse" }}>
                <thead>
                  <tr style={{ background: "#f1f5f9" }}>
                    <th style={th}>Type</th>
                    <th style={th}>Count</th>
                    <th style={th}>Percentage</th>
                  </tr>
                </thead>
                <tbody>
                  {getTypeDistributionWithPercent().map((row) => (
                    <tr key={row.type}>
                      <td style={td}>{row.type}</td>
                      <td style={td}>{row.count}</td>
                      <td style={td}>{row.percentage}%</td>
                    </tr>
                  ))}

                  {/* ---------- TOTAL ROW ---------- */}
                  <tr style={{ fontWeight: "bold", background: "#f8fafc" }}>
                    <td style={td}>Total</td>
                    <td style={td}>{summary.total_count}</td>
                    <td style={td}>100%</td>
                  </tr>
                </tbody>
              </table>

              <p style={{ fontSize: 12, opacity: 0.6, marginTop: 8 }}>
                This table shows the proportional distribution of each equipment
                type relative to the total dataset.
              </p>
            </div>
          </div>


          <div className="card" style={{ width: 500 }}>
            <h4>Average Parameter Values</h4>
            <Bar
              data={{
                labels: ["Flowrate", "Pressure", "Temperature"],
                datasets: [{
                  label: "Average Values",
                  data: [
                    summary.statistics.flowrate.avg,
                    summary.statistics.pressure.avg,
                    summary.statistics.temperature.avg,
                  ],
                  backgroundColor: ["#1498da", "#1498da", "#1498da"],
                }],
              }}
              options={{
                plugins: {
                  tooltip: {
                    callbacks: {
                      label: (ctx) =>
                        `${ctx.label}: ${ctx.parsed.y}`,
                    },
                  },
                },
              }}
            />
          </div>
        </motion.div>
      )}

      {/* ================= PDF PREVIEW ================= */}
      {pdfUrl && (
        <motion.div className="card" style={{ marginTop: 32 }}>
          <h3> PDF Preview</h3>
          <iframe
            src={pdfUrl}
            title="PDF Preview"
            width="100%"
            height="500px"
          />
        </motion.div>
      )}

      {/* ================= HISTORY ================= */}
      <motion.div className="card" style={{ marginTop: 32 }}>
        <h3>🗂 Upload History</h3>

        <input
          placeholder="Search history..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />

          <ul style={{ listStyle: "none", padding: 0 }}>
            {filteredHistory.map((item) => (
              <li
                key={item.id}
                onClick={() => loadSummaryFromHistory(item.id)}
                style={{
                  padding: "10px 14px",
                  marginBottom: 8,
                  cursor: "pointer",
                  borderRadius: 8,
                  background:
                    selectedId === item.id ? "#e0f2fe" : "#f8fafc",
                  border:
                    selectedId === item.id
                      ? "1px solid #38bdf8"
                      : "1px solid #e5e7eb",
                  transition: "all 0.2s ease",
                }}
              >
                <b>{item.name}</b>
              </li>
            ))}
          </ul>

      </motion.div>
    </div>
  );
}


const th = {
  padding: "8px 10px",
  borderBottom: "1px solid #e5e7eb",
  textAlign: "left",
  fontSize: 14,
};

const td = {
  padding: "8px 10px",
  borderBottom: "1px solid #e5e7eb",
  fontSize: 14,
};



