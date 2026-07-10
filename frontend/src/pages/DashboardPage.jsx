import { useEffect, useState } from "react";
import { getKpisSummary } from "../services/api";
import KpiCard from "../components/dashboard/KpiCard";

export default function DashboardPage() {
  const [kpis, setKpis] = useState(null);

  useEffect(() => {
    getKpisSummary().then(setKpis).catch(console.error);
  }, []);

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Dashboard analytique</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <KpiCard label="Chiffre d'affaires" value={kpis?.revenue ?? "—"} />
        <KpiCard label="Commandes" value={kpis?.orders_count ?? "—"} />
        <KpiCard label="Clients" value={kpis?.customers_count ?? "—"} />
      </div>
      {/* TODO: ajouter SalesChart et TopProductsTable */}
    </div>
  );
}
