import React from "react";

/**
 * KpiCard - A premium, self-contained KPI display card.
 * 
 * @param {object} props
 * @param {string} props.label - The label/title of the KPI (e.g. "Chiffre d'affaires").
 * @param {number} props.value - The numeric value of the KPI.
 * @param {"currency" | "number" | "percent"} [props.format] - The formatting style.
 * @param {"currency" | "number" | "text"} [props.type] - Fallback formatting type (for backward compatibility).
 * @param {number} [props.trend] - Optional percentage change value (e.g., 5.4 or -2.1).
 * @param {boolean} [props.isLoading] - Shows pulse skeleton loader if true.
 * @param {React.ReactNode} [props.icon] - Optional icon to display.
 */
export default function KpiCard({
  label,
  value,
  format,
  type,
  trend,
  isLoading,
  icon,
}) {
  // Skeleton loader matching the card structure
  if (isLoading) {
    return (
      <div className="bg-white rounded-2xl border border-slate-100 p-6 shadow-sm animate-pulse flex justify-between items-center w-full min-h-[110px]">
        <div className="space-y-3.5 flex-1">
          <div className="h-4 bg-slate-200 rounded w-1/3"></div>
          <div className="flex items-center gap-3">
            <div className="h-8 bg-slate-200 rounded w-1/2"></div>
            <div className="h-5 bg-slate-200 rounded-full w-12"></div>
          </div>
        </div>
        <div className="h-12 w-12 rounded-xl bg-slate-100 shrink-0"></div>
      </div>
    );
  }

  const isEmpty = value === null || value === undefined || value === "";

  // Formatting helper
  const formatValue = () => {
    if (isEmpty) return null;
    const numValue = Number(value);
    
    if (isNaN(numValue)) return value;

    const activeFormat = format || type || "number";

    if (activeFormat === "currency") {
      return new Intl.NumberFormat("fr-FR", {
        style: "currency",
        currency: "MAD",
        minimumFractionDigits: 2,
      }).format(numValue);
    }

    if (activeFormat === "percent") {
      // Handle potential decimal vs. percentage point difference:
      // If absolute value is > 1 (e.g., 12.5), we scale it to decimal (0.125) for Intl formatting
      const pctValue = Math.abs(numValue) > 1 ? numValue / 100 : numValue;
      return new Intl.NumberFormat("fr-FR", {
        style: "percent",
        minimumFractionDigits: 0,
        maximumFractionDigits: 2,
      }).format(pctValue);
    }

    // Default to number format
    return new Intl.NumberFormat("fr-FR").format(numValue);
  };

  const formattedValue = formatValue();

  // Handle trend calculation and styling
  const hasTrend = trend !== undefined && trend !== null && !isNaN(Number(trend));
  const trendNum = hasTrend ? Number(trend) : 0;
  const isPositive = trendNum > 0;
  const isNegative = trendNum < 0;
  const trendFormatted = hasTrend
    ? new Intl.NumberFormat("fr-FR", {
        minimumFractionDigits: 1,
        maximumFractionDigits: 1,
      }).format(Math.abs(trendNum)) + " %"
    : "";

  return (
    <div className="bg-white rounded-2xl border border-slate-100 p-6 shadow-sm hover:shadow-md hover:border-slate-200 transition-all duration-300 flex justify-between items-center relative overflow-hidden group">
      {/* Decorative background glow on hover */}
      <div className="absolute -right-4 -bottom-4 w-24 h-24 bg-slate-50 rounded-full group-hover:scale-150 transition-transform duration-500 -z-10 opacity-50" />
      
      <div className="space-y-2 z-10 flex-1">
        <p className="text-xs font-bold text-slate-400 tracking-wider uppercase">{label}</p>
        
        <div className="flex items-baseline gap-2.5 flex-wrap">
          {isEmpty ? (
            <p className="text-sm italic text-slate-400 font-normal">Donnée non disponible</p>
          ) : (
            <p className="text-3xl font-extrabold text-slate-900 tracking-tight">
              {formattedValue}
            </p>
          )}
          
          {hasTrend && (
            <div
              className={`inline-flex items-center text-xs font-semibold px-2 py-0.5 rounded-full border ${
                isPositive
                  ? "bg-emerald-50 text-emerald-700 border-emerald-100"
                  : isNegative
                  ? "bg-rose-50 text-rose-700 border-rose-100"
                  : "bg-slate-50 text-slate-600 border-slate-100"
              }`}
            >
              {isPositive && (
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                  className="w-3.5 h-3.5 mr-0.5 shrink-0"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 17a.75.75 0 0 1-.75-.75V5.612L5.29 9.77a.75.75 0 0 1-1.08-1.04l5.25-5.25a.75.75 0 0 1 1.08 0l5.25 5.25a.75.75 0 1 1-1.08 1.04l-3.99-4.158V16.25A.75.75 0 0 1 10 17Z"
                    clipRule="evenodd"
                  />
                </svg>
              )}
              {isNegative && (
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                  className="w-3.5 h-3.5 mr-0.5 shrink-0"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 3a.75.75 0 0 1 .75.75v10.638l3.96-4.158a.75.75 0 1 1 1.08 1.04l-5.25 5.25a.75.75 0 0 1-1.08 0l-5.25-5.25a.75.75 0 1 1 1.08-1.04l3.96 4.158V3.75A.75.75 0 0 1 10 3Z"
                    clipRule="evenodd"
                  />
                </svg>
              )}
              <span>{trendFormatted}</span>
            </div>
          )}
        </div>
      </div>

      {icon && (
        <div className="h-12 w-12 rounded-xl bg-slate-50 flex items-center justify-center text-slate-500 border border-slate-100 group-hover:bg-slate-100 group-hover:text-indigo-600 transition-colors duration-300 shrink-0 ml-4">
          {icon}
        </div>
      )}
    </div>
  );
}

