import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from "chart.js";
import { Line } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

export default function ForecastChart({ predictions = [] }) {
  // Handle empty state
  if (!predictions || predictions.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-6 border border-slate-100 flex flex-col items-center justify-center h-80">
        <p className="text-slate-400 text-sm">Aucune donnée de prévision disponible.</p>
      </div>
    );
  }

  // Sort by date to make sure the line is drawn correctly
  const sortedPredictions = [...predictions].sort((a, b) => new Date(a.date) - new Date(b.date));

  const labels = sortedPredictions.map((item) => item.date || "");
  const dataValues = sortedPredictions.map((item) => item.predicted_sales || 0);

  const chartData = {
    labels,
    datasets: [
      {
        label: "Ventes prévues",
        data: dataValues,
        borderColor: "rgb(139, 92, 246)", // Violet 500
        backgroundColor: "rgba(139, 92, 246, 0.05)", // Violet with opacity
        fill: true,
        tension: 0.3,
        borderDash: [6, 6], // Dashed line for forecast
        pointRadius: 4,
        pointBackgroundColor: "rgb(139, 92, 246)",
        pointBorderColor: "#fff",
        pointBorderWidth: 1.5,
        pointHoverRadius: 6,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        mode: "index",
        intersect: false,
        callbacks: {
          label: function (context) {
            let label = context.dataset.label || "";
            if (label) {
              label += " : ";
            }
            if (context.parsed.y !== null) {
              label += new Intl.NumberFormat("fr-FR", {
                style: "currency",
                currency: "EUR",
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
          color: "#64748b", // slate-500
          font: {
            family: "Outfit, Inter, system-ui, sans-serif",
          },
        },
      },
      y: {
        grid: {
          color: "#f1f5f9", // slate-100
        },
        ticks: {
          color: "#64748b", // slate-500
          font: {
            family: "Outfit, Inter, system-ui, sans-serif",
          },
          callback: function (value) {
            return new Intl.NumberFormat("fr-FR", {
              style: "currency",
              currency: "EUR",
              notation: "compact",
              compactDisplay: "short",
            }).format(value);
          },
        },
      },
    },
  };

  return (
    <div className="bg-white rounded-lg shadow p-6 border border-slate-100">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold text-slate-800">Évolution prévisionnelle</h3>
        <span className="px-2.5 py-0.5 text-xs font-semibold rounded-full bg-violet-50 text-violet-700 border border-violet-100">
          Modèle IA
        </span>
      </div>
      <div className="h-72">
        <Line data={chartData} options={options} />
      </div>
    </div>
  );
}
