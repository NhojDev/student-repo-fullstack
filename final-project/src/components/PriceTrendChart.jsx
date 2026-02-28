// PriceTrendChart.jsx


import { useState } from "react";
import {
  LineChart, Line, XAxis, YAxis,
  CartesianGrid, Tooltip, ResponsiveContainer,
} from "recharts";
import SectionHeader from "./SectionHeader";

// ─── CUSTOM TOOLTIP ───────────────────────────────────────────────────────────
function CustomTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  return (
    <div className="custom-tooltip">
      <p className="tooltip-label">{label}</p>
      {payload.map((p, i) => (
        <p key={i} style={{ color: p.color }}>
          {p.name.toUpperCase()}: {p.value} ₱
        </p>
      ))}
    </div>
  );
}

// ─── COMPONENT ────────────────────────────────────────────────────────────────
export default function PriceTrendChart({ data }) {
  const items = Object.keys(data);
  const [selectedItem, setSelectedItem] = useState(items[0]);
  const trendData = data[selectedItem];

  return (
    <div className="chart-panel">
      <SectionHeader title="Price Trends" subtitle="Buy & Sell over time" />

      {/* Item selector buttons */}
      <div className="item-selector">
        {items.map((item) => (
          <button
            key={item}
            className={`item-btn ${selectedItem === item ? "active" : ""}`}
            onClick={() => setSelectedItem(item)}
          >
            {item}
          </button>
        ))}
      </div>

      {/* Line chart */}
      <ResponsiveContainer width="100%" height={240}>
        <LineChart data={trendData} margin={{ top: 4, right: 16, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(200,160,60,0.08)" />
          <XAxis
            dataKey="date"
            tick={{ fill: "#6b6456", fontSize: 10, fontFamily: "Courier Prime" }}
            axisLine={{ stroke: "rgba(200,160,60,0.2)" }}
            tickLine={false}
          />
          <YAxis
            tick={{ fill: "#6b6456", fontSize: 10, fontFamily: "Courier Prime" }}
            axisLine={false}
            tickLine={false}
            tickFormatter={(v) => `${v}₱`}
          />
          <Tooltip content={<CustomTooltip />} />

          {/* Sell line — solid gold */}
          <Line
            type="monotone" dataKey="sell" name="Sell"
            stroke="#c8a03c" strokeWidth={2}
            dot={{ fill: "#c8a03c", r: 3, strokeWidth: 0 }}
            activeDot={{ r: 5, fill: "#c8a03c", stroke: "rgba(200,160,60,0.4)", strokeWidth: 4 }}
          />

          {/* Buy line — dashed green */}
          <Line
            type="monotone" dataKey="buy" name="Buy"
            stroke="#44c87a" strokeWidth={2}
            dot={{ fill: "#44c87a", r: 3, strokeWidth: 0 }}
            activeDot={{ r: 5, fill: "#44c87a", stroke: "rgba(68,200,122,0.4)", strokeWidth: 4 }}
            strokeDasharray="5 3"
          />
        </LineChart>
      </ResponsiveContainer>

      {/* Legend */}
      <div className="chart-legend">
        {[
          { color: "#c8a03c", label: "SELL ORDERS", dash: false },
          { color: "#44c87a", label: "BUY ORDERS",  dash: true  },
        ].map((l) => (
          <div key={l.label} className="legend-item">
            <svg width={24} height={2}>
              {l.dash
                ? <line x1={0} y1={1} x2={24} y2={1} stroke={l.color} strokeWidth={2} strokeDasharray="5 3" />
                : <line x1={0} y1={1} x2={24} y2={1} stroke={l.color} strokeWidth={2} />
              }
            </svg>
            <span className="legend-label">{l.label}</span>
          </div>
        ))}
      </div>
    </div>
  );
}