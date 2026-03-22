// App.jsx
// Main dashboard shell. Fetches data from FastAPI and passes down to components.

import { useState, useEffect } from "react";
import "./App.css";
import StatCard        from "./components/StatCard";
import PriceTrendChart from "./components/PriceTrendChart";
import SpreadChart     from "./components/SpreadChart";
import TopItemsTable   from "./components/TopItemsTable";
import VolumeBarChart  from "./components/VolumeBarChart";

const API = import.meta.env.VITE_API_URL;

export default function App() {
  const [mounted,      setMounted]      = useState(false);
  const [loading,      setLoading]      = useState(true);
  const [lastUpdated,  setLastUpdated]  = useState(null);
  const [summary,      setSummary]      = useState([]);
  const [topItems,     setTopItems]     = useState([]);
  const [spreads,      setSpreads]      = useState([]);
  const [priceTrends,  setPriceTrends]  = useState({});

  useEffect(() => { setTimeout(() => setMounted(true), 100); }, []);

  // ── Fetch all data on mount ──
  useEffect(() => {
    const fetchAll = async () => {
      try {
        const [summaryRes, topRes, spreadsRes] = await Promise.all([
          fetch(`${API}/api/summary`),
          fetch(`${API}/api/top-items`),
          fetch(`${API}/api/spreads`),
        ]);
        setSummary(await summaryRes.json());
        setTopItems(await topRes.json());
        setSpreads(await spreadsRes.json());
        setLastUpdated(new Date().toLocaleTimeString());
      } catch (err) {
        console.error("Failed to fetch data:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchAll();
  }, []);

  // ── Fetch price trend for a specific item when selected ──
  const fetchPriceTrend = async (itemName) => {
    if (priceTrends[itemName]) return; // already fetched
    try {
      const res  = await fetch(`${API}/api/price-trends?item=${itemName}`);
      const data = await res.json();
      setPriceTrends(prev => ({ ...prev, [itemName]: data.data }));
    } catch (err) {
      console.error("Failed to fetch price trend:", err);
    }
  };

  if (loading) return (
    <div style={{
      color: "#c8a03c", fontFamily: "Courier Prime, monospace",
      padding: 40, background: "#080a0d", minHeight: "100vh",
      letterSpacing: 2, fontSize: 13,
    }}>
      // LOADING DATA...
    </div>
  );

  return (
    <div className="dashboard" style={{ opacity: mounted ? 1 : 0 }}>

      {/* HEADER */}
      <div className="header">
        <div className="header-left">
          <div className="header-eyebrow">// TENNO MARKET INTELLIGENCE</div>
          <div className="header-title">WFM <span>TRACKER</span></div>
          <div className="header-sub">Warframe Market Analytics and Visualizations</div>
        </div>
        <div className="header-status">
          <div className="pulse" />
          {lastUpdated ? `LAST SYNC · ${lastUpdated}` : "CONNECTING..."}
        </div>
      </div>

      {/* STAT CARDS */}
      <div className="stats-grid">
        {summary.map((s, i) => (
          <StatCard key={s.label} {...s} index={i} />
        ))}
      </div>

      {/* PRICE TREND + SPREAD */}
      <div className="charts-grid">
        <PriceTrendChart
          data={priceTrends}
          topItems={topItems}
          onItemSelect={fetchPriceTrend}
        />
        <SpreadChart data={spreads} />
      </div>

      {/* TOP ITEMS TABLE + VOLUME BAR CHART */}
      <div className="bottom-grid">
        <TopItemsTable  data={topItems} />
        <VolumeBarChart data={topItems} />
      </div>

      {/* FOOTER */}
      <div className="footer">
        <span className="footer-text">
          // LIVE DATA · FASTAPI + SUPABASE
        </span>
        <span className="footer-text">
          WARFRAME MARKET ANALYTICS v0.1.0
        </span>
      </div>

    </div>
  );
}