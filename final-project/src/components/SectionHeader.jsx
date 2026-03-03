// SectionHeader.jsx
// The [ TITLE ] header with subtitle and trailing line used above every chart panel.
// Props:
//   title    (string) — main section label e.g. "Price Trends"
//   subtitle (string) — optional smaller label below e.g. "Buy & Sell over time"

export default function SectionHeader({ title, subtitle }) {
  return (
    <div className="section-header">
      <div className="section-bracket">[</div>
      <div>
        <div className="section-title">{title}</div>
        {subtitle && <div className="section-sub">{subtitle}</div>}
      </div>
      <div className="section-bracket">]</div>
      <div className="section-line" />
    </div>
  );
}