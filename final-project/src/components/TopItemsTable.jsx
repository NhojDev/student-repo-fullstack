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
            <th>Volume</th>
            <th>24h Δ</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item, i) => (
            <tr key={item.name}>

              {/* Rank number, zero-padded: 01, 02, etc. */}
              <td>
                <span className="rank-num">
                  {String(i + 1).padStart(2, "0")}
                </span>
              </td>

              {/* Item name */}
              <td className="item-name">{item.name}</td>

              {/* Trade volume */}
              <td className="item-volume">
                {item.volume.toLocaleString()}
              </td>

              {/* 24h change — green if positive, red if negative */}
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