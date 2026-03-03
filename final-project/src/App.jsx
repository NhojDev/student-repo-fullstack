// App.jsx

import { useState, useEffect } from "react";
import StatCard        from "./components/StatCard";
import SectionHeader   from "./components/SectionHeader";
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
  // Controls the page-load fade-in — triggers after first render
  const [mounted, setMounted] = useState(false);
  useEffect(() => { setTimeout(() => setMounted(true), 100); }, []);

  return (
    <>
      {/* ─── ALL COMPONENT STYLES ─────────────────────────────────────────── */}
      <style>{`

        /* DASHBOARD WRAPPER */
        .dashboard {
          max-width: 1400px;
          margin: 0 auto;
          padding: 32px 24px;
          opacity: ${mounted ? 1 : 0};
          transition: opacity 0.4s ease;
        }

        /* ── HEADER ───────────────────────────────────────────────────────── */
        .header {
          display: flex;
          align-items: flex-start;
          justify-content: space-between;
          margin-bottom: 40px;
          padding-bottom: 24px;
          border-bottom: 1px solid var(--border);
        }
        .header-left { display: flex; flex-direction: column; gap: 4px; }
        .header-eyebrow {
          font-family: var(--font-mono);
          font-size: 11px;
          letter-spacing: 3px;
          color: var(--gold);
          text-transform: uppercase;
        }
        .header-title {
          font-size: 36px;
          font-weight: 700;
          letter-spacing: 2px;
          line-height: 1;
          text-transform: uppercase;
          color: #fff;
        }
        .header-title span { color: var(--gold); }
        .header-sub {
          font-size: 13px;
          color: var(--text-dim);
          letter-spacing: 1px;
          margin-top: 4px;
        }
        .header-status {
          display: flex;
          align-items: center;
          gap: 8px;
          font-family: var(--font-mono);
          font-size: 11px;
          color: var(--gold-dim);
          letter-spacing: 1px;
          padding: 8px 14px;
          border: 1px solid var(--border);
          background: var(--gold-faint);
        }
        .pulse {
          width: 8px; height: 8px;
          border-radius: 50%;
          background: var(--green);
          box-shadow: 0 0 6px var(--green);
          animation: pulse 2s ease infinite;
        }

        /* ── STAT CARDS ───────────────────────────────────────────────────── */
        .stats-grid {
          display: grid;
          grid-template-columns: repeat(4, 1fr);
          gap: 12px;
          margin-bottom: 40px;
        }
        .stat-card {
          background: var(--bg2);
          border: 1px solid var(--border);
          border-top: 2px solid var(--gold-dim);
          padding: 18px 20px;
          position: relative;
          overflow: hidden;
          animation: fadeUp 0.5s ease both;
        }
        .stat-card::before {
          content: '';
          position: absolute;
          inset: 0;
          background: var(--gold-faint);
          opacity: 0;
          transition: opacity 0.3s;
        }
        .stat-card:hover::before { opacity: 1; }
        .stat-label {
          font-family: var(--font-mono);
          font-size: 11px;
          letter-spacing: 2px;
          text-transform: uppercase;
          color: var(--text-dim);
          margin-bottom: 8px;
        }
        .stat-value {
          font-size: 28px;
          font-weight: 700;
          color: #fff;
          letter-spacing: 1px;
        }
        .stat-delta { font-family: var(--font-mono); font-size: 12px; margin-top: 4px; }
        .stat-delta.up   { color: var(--green); }
        .stat-delta.down { color: var(--red);   }

        /* ── SECTION HEADER ───────────────────────────────────────────────── */
        .section-header {
          display: flex;
          align-items: center;
          gap: 10px;
          margin-bottom: 18px;
        }
        .section-bracket {
          font-size: 22px;
          color: var(--gold);
          font-family: var(--font-mono);
          line-height: 1;
        }
        .section-title {
          font-size: 16px;
          font-weight: 700;
          letter-spacing: 3px;
          text-transform: uppercase;
          color: var(--gold);
        }
        .section-sub {
          font-size: 11px;
          color: var(--text-dim);
          letter-spacing: 1px;
          font-family: var(--font-mono);
        }
        .section-line {
          flex: 1;
          height: 1px;
          background: linear-gradient(to right, var(--border), transparent);
        }

        /* ── CHART PANELS ─────────────────────────────────────────────────── */
        .chart-panel {
          background: var(--bg2);
          border: 1px solid var(--border);
          padding: 24px;
          animation: fadeUp 0.5s ease both;
          animation-delay: 0.2s;
        }

        /* ── CHARTS GRID (2-col) ──────────────────────────────────────────── */
        .charts-grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 20px;
          margin-bottom: 20px;
        }

        /* ── BOTTOM GRID (table + bar chart) ─────────────────────────────── */
        .bottom-grid {
          display: grid;
          grid-template-columns: 2fr 1fr;
          gap: 20px;
        }

        /* ── ITEM SELECTOR BUTTONS ────────────────────────────────────────── */
        .item-selector {
          display: flex;
          gap: 8px;
          flex-wrap: wrap;
          margin-bottom: 20px;
        }
        .item-btn {
          font-family: var(--font-mono);
          font-size: 11px;
          letter-spacing: 1px;
          padding: 6px 12px;
          border: 1px solid var(--border);
          background: transparent;
          color: var(--text-dim);
          cursor: pointer;
          transition: all 0.2s;
          text-transform: uppercase;
        }
        .item-btn:hover {
          border-color: var(--gold-dim);
          color: var(--gold);
          background: var(--gold-faint);
        }
        .item-btn.active {
          border-color: var(--gold);
          color: var(--gold);
          background: var(--gold-glow);
        }

        /* ── CHART LEGEND ─────────────────────────────────────────────────── */
        .chart-legend  { display: flex; gap: 20px; margin-top: 12px; }
        .legend-item   { display: flex; align-items: center; gap: 6px; }
        .legend-label  {
          font-family: var(--font-mono);
          font-size: 10px;
          color: var(--text-dim);
          letter-spacing: 1px;
        }

        /* ── CUSTOM TOOLTIP ───────────────────────────────────────────────── */
        .custom-tooltip {
          background: rgba(10,10,14,0.95);
          border: 1px solid rgba(200,160,60,0.5);
          padding: 10px 14px;
          font-family: var(--font-mono);
          font-size: 12px;
        }
        .tooltip-label {
          color: var(--gold);
          margin-bottom: 6px;
          letter-spacing: 1px;
        }

        /* ── SPREAD CHART ─────────────────────────────────────────────────── */
        .spread-rows      { display: flex; flex-direction: column; gap: 12px; }
        .spread-row       { display: flex; flex-direction: column; gap: 4px; }
        .spread-labels    { display: flex; justify-content: space-between; font-size: 12px; font-family: var(--font-mono); }
        .spread-item-name { color: var(--text); font-size: 13px; font-weight: 600; font-family: var(--font-display); }
        .spread-amount    { color: var(--text-dim); }
        .spread-value     { color: var(--cyan); }
        .spread-track {
          height: 20px;
          background: var(--bg3);
          border: 1px solid var(--border);
          position: relative;
          overflow: hidden;
        }
        .spread-sell-bar {
          position: absolute; inset-block: 0; left: 0;
          background: linear-gradient(to right, rgba(200,160,60,0.1), rgba(200,160,60,0.4));
          border-right: 2px solid var(--gold);
          transition: width 0.8s ease;
        }
        .spread-buy-bar {
          position: absolute; inset-block: 0; left: 0;
          background: linear-gradient(to right, rgba(68,200,122,0.6), rgba(68,200,122,0.3));
          border-right: 2px solid var(--green);
          transition: width 0.8s ease;
        }
        .spread-buy-price  { color: var(--green); }
        .spread-sell-price { color: var(--gold);  }

        /* ── TOP ITEMS TABLE ──────────────────────────────────────────────── */
        .items-table { width: 100%; border-collapse: collapse; }
        .items-table th {
          font-family: var(--font-mono);
          font-size: 10px;
          letter-spacing: 2px;
          text-transform: uppercase;
          color: var(--gold-dim);
          text-align: left;
          padding: 8px 12px;
          border-bottom: 1px solid var(--border);
        }
        .items-table td {
          padding: 10px 12px;
          font-size: 14px;
          font-weight: 600;
          border-bottom: 1px solid var(--gold-faint);
          transition: background 0.2s;
        }
        .items-table tr:hover td { background: var(--gold-faint); }
        .rank-num   { font-family: var(--font-mono); font-size: 11px; color: var(--text-dim); }
        .item-name  { font-weight: 600; letter-spacing: 0.5px; }
        .item-volume { font-family: var(--font-mono); color: var(--gold); }
        .change-up   { color: var(--green); font-family: var(--font-mono); font-size: 12px; }
        .change-down { color: var(--red);   font-family: var(--font-mono); font-size: 12px; }

        /* ── FOOTER ───────────────────────────────────────────────────────── */
        .footer {
          margin-top: 32px;
          padding-top: 16px;
          border-top: 1px solid rgba(200,160,60,0.1);
          display: flex;
          justify-content: space-between;
          align-items: center;
        }
        .footer-text {
          font-family: var(--font-mono);
          font-size: 10px;
          color: #3a3530;
          letter-spacing: 1px;
        }

        /* ── RESPONSIVE ───────────────────────────────────────────────────── */
        @media (max-width: 900px) {
          .stats-grid   { grid-template-columns: repeat(2, 1fr); }
          .charts-grid  { grid-template-columns: 1fr; }
          .bottom-grid  { grid-template-columns: 1fr; }
          .header       { flex-direction: column; gap: 16px; }
          .header-title { font-size: 28px; }
        }
      `}</style>

      {/* ─── DASHBOARD ──────────────────────────────────────────────────────── */}
      <div className="dashboard">

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

        {/* PRICE TREND + SPREAD (2 columns) */}
        <div className="charts-grid">
          <PriceTrendChart data={PRICE_TRENDS} />
          <SpreadChart data={SPREAD_DATA} />
        </div>

        {/* TOP ITEMS TABLE + VOLUME BAR CHART */}
        <div className="bottom-grid">
          <TopItemsTable   data={TOP_ITEMS} />
          <VolumeBarChart  data={TOP_ITEMS} />
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
    </>
  );
}