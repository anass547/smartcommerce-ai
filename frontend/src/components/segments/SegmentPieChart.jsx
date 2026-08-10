import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import { Doughnut } from "react-chartjs-2";

ChartJS.register(ArcElement, Tooltip, Legend);

// Premium color mapping per RFM segment
const SEGMENT_COLORS = {
  VIP: {
    bg: "rgba(99, 102, 241, 0.85)", // Indigo
    border: "rgb(99, 102, 241)",
  },
  Fidèles: {
    bg: "rgba(20, 184, 166, 0.85)", // Teal
    border: "rgb(20, 184, 166)",
  },
  Occasionnels: {
    bg: "rgba(14, 165, 233, 0.85)", // Sky Blue
    border: "rgb(14, 165, 233)",
  },
  "À risque": {
    bg: "rgba(244, 63, 94, 0.85)", // Rose
    border: "rgb(244, 63, 94)",
  },
};

const DEFAULT_COLOR_PALETTE = [
  { bg: "rgba(99, 102, 241, 0.85)", border: "rgb(99, 102, 241)" },
  { bg: "rgba(20, 184, 166, 0.85)", border: "rgb(20, 184, 166)" },
  { bg: "rgba(14, 165, 233, 0.85)", border: "rgb(14, 165, 233)" },
  { bg: "rgba(244, 63, 94, 0.85)", border: "rgb(244, 63, 94)" },
];

export default function SegmentPieChart({ segments = [] }) {
  const totalCount = segments.reduce((sum, s) => sum + (s.count || 0), 0);

  if (!segments || segments.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-6 border border-slate-100 flex flex-col items-center justify-center h-96 mt-6">
        <p className="text-slate-400 text-sm">Aucune donnée de segmentation disponible.</p>
      </div>
    );
  }

  const labels = segments.map((s) => s.name);
  const dataValues = segments.map((s) => s.count || 0);

  const backgroundColors = segments.map((s, idx) => {
    return SEGMENT_COLORS[s.name]?.bg || DEFAULT_COLOR_PALETTE[idx % DEFAULT_COLOR_PALETTE.length].bg;
  });

  const borderColors = segments.map((s, idx) => {
    return SEGMENT_COLORS[s.name]?.border || DEFAULT_COLOR_PALETTE[idx % DEFAULT_COLOR_PALETTE.length].border;
  });

  const chartData = {
    labels,
    datasets: [
      {
        data: dataValues,
        backgroundColor: backgroundColors,
        borderColor: borderColors,
        borderWidth: 2,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: "bottom",
        labels: {
          color: "#475569", // slate-600
          padding: 20,
          usePointStyle: true,
          pointStyle: "circle",
          font: {
            family: "Outfit, Inter, system-ui, sans-serif",
            size: 13,
            weight: "500",
          },
        },
      },
      tooltip: {
        callbacks: {
          label: function (context) {
            const val = context.raw;
            const pct = totalCount > 0 ? ((val / totalCount) * 100).toFixed(1) : 0;
            return ` ${context.label}: ${new Intl.NumberFormat("fr-FR").format(val)} clients (${pct}%)`;
          },
        },
      },
    },
    cutout: "65%", // Doughnut cutout
  };

  return (
    <div className="bg-white rounded-lg shadow p-6 border border-slate-100 mt-6 flex flex-col items-center">
      <h3 className="text-lg font-semibold text-slate-800 self-start mb-6">Répartition des segments</h3>
      <div className="w-full h-80 relative flex items-center justify-center">
        {totalCount === 0 ? (
          <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
            <span className="text-4xl font-bold text-slate-300">0%</span>
            <span className="text-xs text-slate-400 mt-1">En attente de calcul RFM</span>
          </div>
        ) : (
          <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none mb-12">
            <span className="text-3xl font-extrabold text-slate-800">
              {new Intl.NumberFormat("fr-FR").format(totalCount)}
            </span>
            <span className="text-xs text-slate-400 mt-0.5">Total clients</span>
          </div>
        )}
        <Doughnut data={chartData} options={options} />
      </div>
    </div>
  );
}
