// App.jsx
import { useState, useEffect } from "react";
import "./App.css";

import StatCard        from "./components/StatCard";
import PriceTrendChart from "./components/PriceTrendChart";
import SpreadChart     from "./components/SpreadChart";
import TopItemsTable   from "./components/TopItemsTable";
import VolumeBarChart  from "./components/VolumeBarChart";

import {
  PRICE_TRENDS,
  TOP_ITEMS,
  SPREAD_DATA,
  STATS_SUMMARY,
} from "./data/mockData";

export default function App() {
  const [mounted, setMounted] = useState(false);
  useEffect(() => { setTimeout(() => setMounted(true), 100); }, []);

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
          DATA SYNC · PLACEHOLDER
        </div>
      </div>

      {/* STAT CARDS */}
      <div className="stats-grid">
        {STATS_SUMMARY.map((s, i) => (
          <StatCard key={s.label} {...s} index={i} />
        ))}
      </div>

      {/* PRICE TREND + SPREAD */}
      <div className="charts-grid">
        <PriceTrendChart data={PRICE_TRENDS} />
        <SpreadChart data={SPREAD_DATA} />
      </div>

      {/* TOP ITEMS TABLE + VOLUME BAR CHART */}
      <div className="bottom-grid">
        <TopItemsTable  data={TOP_ITEMS} />
        <VolumeBarChart data={TOP_ITEMS} />
      </div>

      {/* FOOTER */}
      <div className="footer">
        <span className="footer-text">
          // MOCK DATA · REPLACE WITH FASTAPI + SUPABASE ENDPOINTS
        </span>
        <span className="footer-text">
          WARFRAME MARKET ANALYTICS v0.1.0
        </span>
      </div>

    </div>
  );
}