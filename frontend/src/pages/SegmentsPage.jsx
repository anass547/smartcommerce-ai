import { useEffect, useState } from "react";
import { getSegments } from "../services/api";
import SegmentPieChart from "../components/segments/SegmentPieChart";

export default function SegmentsPage() {
  const [segments, setSegments] = useState([]);

  useEffect(() => {
    getSegments().then((data) => setSegments(data.segments)).catch(console.error);
  }, []);

  const getCardStyle = (name) => {
    switch (name) {
      case "VIP":
        return "border-l-4 border-l-indigo-500";
      case "Fidèles":
        return "border-l-4 border-l-teal-500";
      case "Occasionnels":
        return "border-l-4 border-l-sky-500";
      case "À risque":
        return "border-l-4 border-l-rose-500";
      default:
        return "border border-slate-100";
    }
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Segmentation clients</h1>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {segments.map((s) => (
          <div key={s.name} className={`bg-white rounded-lg shadow p-4 flex flex-col justify-center border border-slate-100/50 ${getCardStyle(s.name)}`}>
            <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">{s.name}</p>
            <p className="text-2xl font-extrabold text-slate-800 mt-1">{new Intl.NumberFormat("fr-FR").format(s.count || 0)}</p>
          </div>
        ))}
      </div>
      <SegmentPieChart segments={segments} />
    </div>
  );
}

