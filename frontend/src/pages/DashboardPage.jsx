import { useEffect, useState } from "react";
import { getKpisSummary } from "../services/api";
import KpiCard from "../components/dashboard/KpiCard";
import SalesChart from "../components/dashboard/SalesChart";
import TopProductsTable from "../components/dashboard/TopProductsTable";

export default function DashboardPage() {
  const [kpis, setKpis] = useState(null);

  useEffect(() => {
    getKpisSummary().then(setKpis).catch(console.error);
  }, []);

  const formattedRevenue = kpis && kpis.revenue !== undefined
    ? new Intl.NumberFormat("fr-FR", { style: "currency", currency: "EUR" }).format(kpis.revenue)
    : "—";

  const formattedOrders = kpis && kpis.orders_count !== undefined
    ? new Intl.NumberFormat("fr-FR").format(kpis.orders_count)
    : "—";

  const formattedCustomers = kpis && kpis.customers_count !== undefined
    ? new Intl.NumberFormat("fr-FR").format(kpis.customers_count)
    : "—";

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Dashboard analytique</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <KpiCard label="Chiffre d'affaires" value={formattedRevenue} />
        <KpiCard label="Commandes" value={formattedOrders} />
        <KpiCard label="Clients" value={formattedCustomers} />
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
        <SalesChart />
        <TopProductsTable products={kpis?.top_products || []} />
      </div>
    </div>
  );
}

