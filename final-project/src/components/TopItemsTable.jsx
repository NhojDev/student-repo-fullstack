// TopItemsTable.jsx


import SectionHeader from "./SectionHeader";

export default function TopItemsTable({ data }) {
  return (
    <div className="chart-panel">
      <SectionHeader title="Top Traded Items" subtitle="By order volume · last 24h" />

      <table className="items-table">
        <thead>
          <tr>
            <th>#</th>
            <th>Item</th>
            <th>Sell</th>
            <th>Buy</th>
            <th>24h Δ</th>
          </tr>
        </thead>
        <tbody>
          {data.slice(0, 10).map((item, i) => (
            <tr key={item.name}>
              <td><span className="rank-num">{String(i + 1).padStart(2, "0")}</span></td>
              <td className="item-name">{item.name.replace(/_/g, " ")}</td>
              <td className="item-volume">{item.sell_listings?.toLocaleString()}</td>
              <td className="item-volume">{item.buy_listings?.toLocaleString()}</td>
              <td>
                <span className={item.change >= 0 ? "change-up" : "change-down"}>
                  {item.change >= 0 ? "▲" : "▼"} {Math.abs(item.change)}%
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}