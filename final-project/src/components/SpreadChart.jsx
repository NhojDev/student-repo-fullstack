// SpreadChart.jsx

import SectionHeader from "./SectionHeader";

export default function SpreadChart({ data }) {
  // Find the highest sell price to use as 100% width reference
  const maxVal = Math.max(...data.map((r) => r.sell));

  return (
    <div className="chart-panel">
      <SectionHeader title="Order Spreads" subtitle="Buy vs Sell gap per item" />

      <div className="spread-rows">
        {data.map((row) => {
          const buyPct  = (row.buy  / maxVal) * 100;
          const sellPct = (row.sell / maxVal) * 100;

          return (
            <div key={row.item} className="spread-row">

              {/* Item name + spread value */}
              <div className="spread-labels">
                <span className="spread-item-name">{row.item}</span>
                <span className="spread-amount">
                  spread: <span className="spread-value">+{row.spread}₱</span>
                </span>
              </div>

              {/* Layered bar track: sell bar behind, buy bar on top */}
              <div className="spread-track">
                <div className="spread-sell-bar" style={{ width: `${sellPct}%` }} />
                <div className="spread-buy-bar"  style={{ width: `${buyPct}%`  }} />
              </div>

              {/* Buy and sell price labels */}
              <div className="spread-labels">
                <span className="spread-buy-price">B: {row.buy}₱</span>
                <span className="spread-sell-price">S: {row.sell}₱</span>
              </div>

            </div>
          );
        })}
      </div>
    </div>
  );
}