// VolumeBarChart.jsx

import {
  BarChart, Bar, Cell,
  XAxis, YAxis, Tooltip,
  ResponsiveContainer, CartesianGrid,
} from "recharts";
import SectionHeader from "./SectionHeader";

// ─── CUSTOM TOOLTIP ───────────────────────────────────────────────────────────
function CustomTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  return (
    <div className="custom-tooltip">
      <p className="tooltip-label">{label}</p>
      <p style={{ color: "#d4cbb8" }}>VOLUME: {payload[0].value}</p>
    </div>
  );
}

// ─── COMPONENT ────────────────────────────────────────────────────────────────
export default function VolumeBarChart({ data }) {
  const chartData = data.slice(0, 6);

  return (
    <div className="chart-panel">
      <SectionHeader title="Volume Chart" subtitle="Orders by item" />

      <ResponsiveContainer width="100%" height={295}>
        <BarChart
          data={chartData}
          layout="vertical"
          margin={{ top: 0, right: 16, left: 0, bottom: 0 }}
        >
          <CartesianGrid
            strokeDasharray="3 3"
            stroke="rgba(200,160,60,0.06)"
            horizontal={false}
          />
          <XAxis
            type="number"
            tick={{ fill: "#6b6456", fontSize: 10, fontFamily: "Courier Prime" }}
            axisLine={false}
            tickLine={false}
          />
          <YAxis
            type="category"
            dataKey="name"
            tick={{ fill: "#9a8f7a", fontSize: 10, fontFamily: "Rajdhani", fontWeight: 600 }}
            axisLine={false}
            tickLine={false}
            width={110}
            // Truncate long item names so they fit in the sidebar
            tickFormatter={(v) => v.length > 14 ? v.slice(0, 13) + "…" : v}
          />
          <Tooltip
            cursor={{ fill: "rgba(200,160,60,0.04)" }}
            content={<CustomTooltip />}
          />
          <Bar dataKey="volume" radius={[0, 2, 2, 0]}>
            {chartData.map((entry, index) => (
              <Cell
                key={index}
                // #1 item = full gold, #2 = medium gold, rest = faint
                fill={
                  index === 0 ? "#c8a03c" :
                  index === 1 ? "#a07830" :
                  "rgba(200,160,60,0.35)"
                }
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}