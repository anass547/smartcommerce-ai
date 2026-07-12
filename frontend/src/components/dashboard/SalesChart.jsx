import React, { useRef, useEffect, useState } from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
  Filler,
} from "chart.js";
import { Line } from "react-chartjs-2";

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
  Filler
);

/**
 * SalesChart - A line chart showing sales over time.
 * 
 * @param {object} props
 * @param {Array} props.data - Array of { date: string, revenue: number } objects.
 * @param {boolean} props.isLoading - Shows skeleton loader if true.
 */
export default function SalesChart({ data = [], isLoading }) {
  const chartRef = useRef(null);
  const [chartData, setChartData] = useState(null);

  // Parse and check if data actually has valid entries
  const cleanData = (data || []).filter(
    (item) => item && item.date && item.date.trim() !== ""
  );
  
  const hasData = cleanData.length > 0;

  useEffect(() => {
    if (isLoading || !hasData) return;

    const chart = chartRef.current;
    if (!chart) return;

    const ctx = chart.ctx;
    // Create a beautiful fade gradient for the area under the curve
    const gradient = ctx.createLinearGradient(0, 0, 0, 240);
    gradient.addColorStop(0, "rgba(99, 102, 241, 0.25)"); // Indigo-500 with opacity
    gradient.addColorStop(1, "rgba(99, 102, 241, 0.005)"); // Faded to near-zero

    setChartData({
      labels: cleanData.map((item) => {
        // Format date to French locale style if possible (e.g. DD/MM/YYYY)
        try {
          const dateObj = new Date(item.date);
          if (isNaN(dateObj.getTime())) return item.date;
          return new Intl.DateTimeFormat("fr-FR", {
            day: "numeric",
            month: "short",
          }).format(dateObj);
        } catch {
          return item.date;
        }
      }),
      datasets: [
        {
          label: "Chiffre d'affaires",
          data: cleanData.map((item) => item.revenue),
          borderColor: "#6366f1", // Indigo-500
          borderWidth: 2.5,
          backgroundColor: gradient,
          fill: true,
          tension: 0.3, // Smooth Bezier curves (tension ~0.3)
          pointBackgroundColor: "#4f46e5", // Indigo-600
          pointBorderColor: "#ffffff",
          pointBorderWidth: 2,
          pointRadius: 3,
          pointHoverRadius: 6,
          pointHoverBackgroundColor: "#4f46e5",
          pointHoverBorderColor: "#ffffff",
          pointHoverBorderWidth: 2,
        },
      ],
    });
  }, [cleanData, isLoading, hasData]);

  // Skeleton state
  if (isLoading) {
    return (
      <div className="bg-white rounded-2xl border border-slate-100 p-6 shadow-sm animate-pulse w-full flex flex-col min-h-[320px]">
        <div className="h-4 bg-slate-200 rounded w-1/4 mb-6"></div>
        <div className="h-64 bg-slate-50 border border-dashed border-slate-100 rounded-xl flex items-end p-4 justify-between gap-2 flex-1">
          <div className="h-1/4 bg-slate-200 rounded w-full"></div>
          <div className="h-1/2 bg-slate-200 rounded w-full"></div>
          <div className="h-2/3 bg-slate-200 rounded w-full"></div>
          <div className="h-3/4 bg-slate-200 rounded w-full"></div>
          <div className="h-1/2 bg-slate-200 rounded w-full"></div>
          <div className="h-5/6 bg-slate-200 rounded w-full"></div>
          <div className="h-2/3 bg-slate-200 rounded w-full"></div>
        </div>
      </div>
    );
  }

  // Chart configuration options
  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false, // Custom header handles label
      },
      tooltip: {
        backgroundColor: "#0f172a", // Slate-900
        titleColor: "#f8fafc", // Slate-50
        bodyColor: "#e2e8f0", // Slate-200
        padding: 12,
        borderRadius: 8,
        displayColors: false,
        callbacks: {
          label: (context) => {
            let label = context.dataset.label || "";
            if (label) {
              label += " : ";
            }
            if (context.parsed.y !== null) {
              label += new Intl.NumberFormat("fr-FR", {
                style: "currency",
                currency: "MAD",
              }).format(context.parsed.y);
            }
            return label;
          },
        },
      },
    },
    scales: {
      x: {
        grid: {
          display: false,
        },
        ticks: {
          color: "#64748b", // Slate-500
          font: {
            family: "'Inter', sans-serif",
            size: 11,
          },
        },
      },
      y: {
        border: {
          dash: [4, 4],
        },
        grid: {
          color: "rgba(226, 232, 240, 0.6)", // Slate-200 with opacity
        },
        ticks: {
          color: "#64748b", // Slate-500
          font: {
            family: "'Inter', sans-serif",
            size: 11,
          },
          callback: (value) => {
            return new Intl.NumberFormat("fr-FR", {
              notation: "compact",
              compactDisplay: "short",
              style: "currency",
              currency: "MAD",
            }).format(value);
          },
        },
      },
    },
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-100 p-6 shadow-sm hover:shadow-md hover:border-slate-200 transition-all duration-300 w-full flex flex-col">
      <h2 className="text-xs font-bold text-slate-400 tracking-wider uppercase mb-6">
        Évolution des ventes
      </h2>
      <div className="h-64 w-full relative flex items-center justify-center">
        {!hasData ? (
          <p className="text-sm font-medium text-slate-400 text-center">
            Aucune donnée disponible pour le moment
          </p>
        ) : (
          chartData && <Line ref={chartRef} data={chartData} options={options} />
        )}
      </div>
    </div>
  );
}
