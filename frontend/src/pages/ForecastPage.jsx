import { useEffect, useState } from "react";
import { getForecast } from "../services/api";
import ForecastChart from "../components/forecast/ForecastChart";

export default function ForecastPage() {
  const [horizon, setHorizon] = useState("week");
  const [forecast, setForecast] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    getForecast(horizon)
      .then((data) => {
        setForecast(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, [horizon]);

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Prévision des ventes</h1>
      <div className="flex gap-2 mb-4">
        {["day", "week", "month"].map((h) => (
          <button
            key={h}
            onClick={() => setHorizon(h)}
            className={`px-3 py-1 rounded transition-colors text-sm font-medium ${
              horizon === h ? "bg-slate-900 text-white" : "bg-slate-100 text-slate-700 hover:bg-slate-200"
            }`}
          >
            {h === "day" ? "Jour" : h === "week" ? "Semaine" : "Mois"}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="bg-white rounded-lg shadow p-6 border border-slate-100 flex flex-col items-center justify-center h-80 animate-pulse">
          <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-slate-900 mb-4"></div>
          <p className="text-slate-500 text-sm">Chargement des prévisions...</p>
        </div>
      ) : (
        <ForecastChart predictions={forecast?.predictions ?? []} />
      )}
    </div>
  );
}

