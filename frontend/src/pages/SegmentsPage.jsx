import { useEffect, useState } from "react";
import { getSegments } from "../services/api";

export default function SegmentsPage() {
  const [segments, setSegments] = useState([]);

  useEffect(() => {
    getSegments().then((data) => setSegments(data.segments)).catch(console.error);
  }, []);

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Segmentation clients</h1>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {segments.map((s) => (
          <div key={s.name} className="bg-white rounded-lg shadow p-4 text-center">
            <p className="text-sm text-slate-500">{s.name}</p>
            <p className="text-xl font-bold">{s.count}</p>
          </div>
        ))}
      </div>
      {/* TODO: remplacer par SegmentPieChart (Chart.js) */}
    </div>
  );
}
