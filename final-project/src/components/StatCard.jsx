export default function StatCard({ label, value, delta, up, index }) {
  return (
    <div className="stat-card" style={{ animationDelay: `${index * 0.1}s` }}>
      <div className="stat-label">{label}</div>
      <div className="stat-value">{value}</div>
      <div className={`stat-delta ${up ? "up" : "down"}`}>{delta}</div>
    </div>
  );
}