import { useEffect, useState } from "react";
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
import { getSalesEvolution } from "../../services/api";

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

export default function SalesChart() {
  const [salesData, setSalesData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    getSalesEvolution()
      .then((res) => {
        // Robust handling of response format (object with data key, or direct array)
        const rawData = res && Array.isArray(res.data) ? res.data : (Array.isArray(res) ? res : []);
        setSalesData(rawData);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching sales evolution:", err);
        setError("Erreur lors de la récupération de l'évolution des ventes.");
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow p-6 border border-slate-100 flex flex-col items-center justify-center h-80">
        <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-slate-900 mb-4"></div>
        <p className="text-slate-500 text-sm">Chargement du graphique...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white rounded-lg shadow p-6 border border-slate-100 flex flex-col items-center justify-center h-80">
        <p className="text-red-500 text-sm font-medium mb-2">{error}</p>
        <button
          onClick={() => {
            setLoading(true);
            setError(null);
            getSalesEvolution()
              .then((res) => {
                const rawData = res && Array.isArray(res.data) ? res.data : (Array.isArray(res) ? res : []);
                setSalesData(rawData);
                setLoading(false);
              })
              .catch((err) => {
                console.error(err);
                setError("Erreur lors de la récupération de l'évolution des ventes.");
                setLoading(false);
              });
          }}
          className="px-3 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs rounded transition-colors"
        >
          Réessayer
        </button>
      </div>
    );
  }

  // Handle case where salesData is empty
  if (salesData.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-6 border border-slate-100 flex flex-col items-center justify-center h-80">
        <p className="text-slate-400 text-sm">Aucune donnée de ventes disponible.</p>
      </div>
    );
  }

  // Parse labels and values
  const labels = salesData.map((item) => item.date || item.ds || "");
  const dataValues = salesData.map((item) => (item.revenue !== undefined ? item.revenue : (item.y !== undefined ? item.y : 0)));

  const chartData = {
    labels,
    datasets: [
      {
        label: "Chiffre d'affaires",
        data: dataValues,
        borderColor: "rgb(71, 85, 105)", // Slate 600
        backgroundColor: "rgba(71, 85, 105, 0.05)", // Slate 600 with opacity
        fill: true,
        tension: 0.2,
        pointRadius: labels.length > 30 ? 0 : 3,
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
          maxTicksLimit: 8,
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
      <h3 className="text-lg font-semibold text-slate-800 mb-4">Évolution des ventes</h3>
      <div className="h-64">
        <Line data={chartData} options={options} />
      </div>
    </div>
  );
}
