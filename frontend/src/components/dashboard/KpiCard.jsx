import { DollarSign, ShoppingBag, Users, ArrowUpRight, ArrowDownRight } from "lucide-react";

export default function KpiCard({ label, value, icon, trend }) {
  // Mapping icon names to Lucide icons
  const IconComponent = {
    revenue: DollarSign,
    orders: ShoppingBag,
    customers: Users,
  }[icon] || DollarSign;

  return (
    <div className="bg-white rounded-lg shadow-sm p-5 border border-slate-100 border-t-4 border-t-indigo-500/90 relative flex flex-col justify-between h-32 transition-all hover:shadow-md hover:-translate-y-0.5 duration-300">
      <div className="flex justify-between items-start w-full">
        <div className="flex-1">
          <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">{label}</p>
          <p className="text-3xl font-extrabold text-slate-900 tracking-tight mt-1.5 leading-none">
            {value}
          </p>
        </div>
        <div className="p-2 bg-indigo-50/60 text-indigo-600 rounded-lg border border-indigo-100/30">
          <IconComponent className="h-5 w-5" />
        </div>
      </div>
      
      {trend ? (
        <div className="flex items-center gap-1.5 text-xs">
          {trend.isPositive ? (
            <span className="flex items-center font-bold text-emerald-600 bg-emerald-50/80 px-2 py-0.5 rounded-full border border-emerald-100/50">
              <ArrowUpRight className="h-3.5 w-3.5 mr-0.5 stroke-[2.5]" />
              {trend.value}
            </span>
          ) : (
            <span className="flex items-center font-bold text-rose-600 bg-rose-50/80 px-2 py-0.5 rounded-full border border-rose-100/50">
              <ArrowDownRight className="h-3.5 w-3.5 mr-0.5 stroke-[2.5]" />
              {trend.value}
            </span>
          )}
          <span className="text-slate-400 font-normal">vs période précédente</span>
        </div>
      ) : (
        <div className="h-5"></div>
      )}
    </div>
  );
}
