export default function KpiCard({ label, value }) {
  return (
    <div className="bg-white rounded-lg shadow p-4 border border-slate-100">
      <p className="text-sm text-slate-500">{label}</p>
      <p className="text-2xl font-bold text-slate-900">{value}</p>
    </div>
  );
}
