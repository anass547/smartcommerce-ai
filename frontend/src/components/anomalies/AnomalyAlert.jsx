export default function AnomalyAlert({ anomalies = [] }) {
  if (!anomalies || anomalies.length === 0) return null;

  return (
    <div className="flex flex-col gap-3 mb-6">
      {anomalies.map((anomaly, index) => {
        const dateStr = anomaly.date || "";
        const messageStr = anomaly.message || "";
        const deviation = anomaly.deviation_pct !== undefined ? `${anomaly.deviation_pct}%` : "";

        return (
          <div
            key={index}
            className="bg-amber-50 border-l-4 border-amber-500 text-amber-800 p-4 rounded-r-lg shadow-sm flex items-start gap-3 transition-all hover:shadow-md animate-fade-in"
          >
            {/* Warning Icon */}
            <div className="flex-shrink-0 mt-0.5">
              <svg
                className="h-5 w-5 text-amber-600"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth="2"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                />
              </svg>
            </div>
            
            {/* Alert Content */}
            <div className="flex-1 flex flex-col md:flex-row md:items-center md:justify-between gap-2">
              <div>
                <p className="font-semibold text-amber-900 text-sm">
                  Variation anormale {deviation && `(${deviation})`}
                </p>
                <p className="text-sm text-amber-800 mt-0.5">{messageStr}</p>
              </div>
              {dateStr && (
                <span className="text-xs font-semibold text-amber-600 bg-amber-100/50 border border-amber-200/50 px-2 py-0.5 rounded-md self-start md:self-center">
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
