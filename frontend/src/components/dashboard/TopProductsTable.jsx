import React from "react";

/**
 * TopProductsTable - A table displaying the top products by units sold and revenue.
 * 
 * @param {object} props
 * @param {Array} props.products - Array of { name: string, revenue: number, units_sold: number } objects.
 * @param {boolean} props.isLoading - Shows skeleton loader if true.
 */
export default function TopProductsTable({ products = [], isLoading }) {
  // Filter out invalid product items
  const cleanProducts = (products || []).filter(
    (product) => product && product.name && product.name.trim() !== ""
  );

  const hasData = cleanProducts.length > 0;

  // Find max units sold to calculate relative progress bar widths
  const maxUnitsSold = Math.max(
    ...cleanProducts.map((p) => p.units_sold || 0),
    1
  );

  // Skeleton state
  if (isLoading) {
    return (
      <div className="bg-white rounded-2xl border border-slate-100 p-6 shadow-sm animate-pulse w-full flex flex-col min-h-[320px]">
        <div className="h-4 bg-slate-200 rounded w-1/4 mb-6"></div>
        <div className="space-y-4 flex-1">
          {[1, 2, 3, 4, 5].map((i) => (
            <div key={i} className="flex justify-between items-center gap-4 py-2">
              <div className="space-y-2 flex-1">
                <div className="h-4 bg-slate-200 rounded w-2/3"></div>
                <div className="h-2 bg-slate-100 rounded w-1/3"></div>
              </div>
              <div className="h-4 bg-slate-200 rounded w-12"></div>
              <div className="h-4 bg-slate-200 rounded w-16"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-2xl border border-slate-100 p-6 shadow-sm hover:shadow-md hover:border-slate-200 transition-all duration-300 w-full flex flex-col justify-between">
      <div>
        <h2 className="text-xs font-bold text-slate-400 tracking-wider uppercase mb-6">
          Top produits
        </h2>

        {!hasData ? (
          <div className="h-64 flex items-center justify-center">
            <p className="text-sm font-medium text-slate-400 text-center">
              Aucun produit à afficher pour le moment
            </p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-slate-100 text-xs font-semibold text-slate-500 uppercase">
                  <th className="pb-3 pl-1 text-left">Produit</th>
                  <th className="pb-3 text-right">Unités vendues</th>
                  <th className="pb-3 text-right pr-1">CA</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-50">
                {cleanProducts.map((product, index) => {
                  const percentage = ((product.units_sold || 0) / maxUnitsSold) * 100;
                  
                  return (
                    <tr key={index} className="group hover:bg-slate-50/50 transition-colors duration-150">
                      <td className="py-3.5 pl-1 max-w-[180px] sm:max-w-none">
                        <div className="flex flex-col">
                          <span className="font-semibold text-slate-800 text-sm group-hover:text-indigo-650 transition-colors duration-150 truncate">
                            {product.name}
                          </span>
                          {/* Mini progress bar under the product name */}
                          <div className="w-24 bg-slate-100 h-1.5 rounded-full mt-1.5 overflow-hidden">
                            <div
                              className="bg-indigo-500 h-full rounded-full transition-all duration-500"
                              style={{ width: `${percentage}%` }}
                            />
                          </div>
                        </div>
                      </td>
                      <td className="py-3.5 text-right font-medium text-slate-500 text-sm">
                        {new Intl.NumberFormat("fr-FR").format(product.units_sold || 0)}
                      </td>
                      <td className="py-3.5 text-right font-bold text-slate-900 text-sm pr-1">
                        {new Intl.NumberFormat("fr-FR", {
                          style: "currency",
                          currency: "MAD",
                        }).format(product.revenue || 0)}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
