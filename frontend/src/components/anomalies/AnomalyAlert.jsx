import { AlertTriangle } from "lucide-react";

export default function AnomalyAlert({ anomalies = [] }) {
  if (!anomalies || anomalies.length === 0) return null;

  return (
    <div className="flex flex-col gap-3.5 mb-6">
      {anomalies.map((anomaly, index) => {
        const dateStr = anomaly.date || "";
        const messageStr = anomaly.message || "";
        const deviation = anomaly.deviation_pct !== undefined ? `${anomaly.deviation_pct}%` : "";

        return (
          <div
            key={index}
            className="bg-amber-50/70 border border-amber-200 border-l-4 border-l-amber-500 p-4 rounded-r-lg shadow-sm flex items-start gap-3.5 transition-all hover:shadow-md duration-300"
          >
            {/* Warning Icon Container */}
            <div className="flex-shrink-0 p-1.5 bg-amber-100 text-amber-600 rounded-md border border-amber-200/40">
              <AlertTriangle className="h-4.5 w-4.5 stroke-[2.5]" />
            </div>
            
            {/* Alert Content */}
            <div className="flex-1 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
              <div>
                <p className="font-bold text-amber-900 text-sm">
                  Variation anormale détectée {deviation && `(${deviation})`}
                </p>
                <p className="text-sm text-amber-800 mt-1 font-medium leading-relaxed">
                  {messageStr}
                </p>
              </div>
              {dateStr && (
                <span className="text-xs font-bold text-amber-700 bg-amber-100/50 border border-amber-200/50 px-2.5 py-1 rounded-md self-start sm:self-center font-mono">
                  {dateStr}
                </span>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}
