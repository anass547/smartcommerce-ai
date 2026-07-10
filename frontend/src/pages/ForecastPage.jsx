import { useEffect, useState } from "react";
import { getForecast } from "../services/api";

export default function ForecastPage() {
  const [horizon, setHorizon] = useState("week");
  const [forecast, setForecast] = useState(null);

  useEffect(() => {
    getForecast(horizon).then(setForecast).catch(console.error);
  }, [horizon]);

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Prévision des ventes</h1>
      <div className="flex gap-2 mb-4">
        {["day", "week", "month"].map((h) => (
          <button
            key={h}
            onClick={() => setHorizon(h)}
            className={`px-3 py-1 rounded ${
              horizon === h ? "bg-slate-900 text-white" : "bg-slate-100"
            }`}
          >
            {h}
          </button>
        ))}
      </div>
      {/* TODO: remplacer par ForecastChart (Chart.js) avec forecast.predictions */}
      <pre className="text-sm text-slate-500">{JSON.stringify(forecast, null, 2)}</pre>
    </div>
  );
}
