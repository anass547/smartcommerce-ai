export default function TopProductsTable({ products = [] }) {
  if (!products || products.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-6 border border-slate-100 flex flex-col items-center justify-center h-80">
        <h3 className="text-lg font-semibold text-slate-800 self-start mb-4">Top Produits</h3>
        <div className="flex-1 flex items-center justify-center w-full">
          <p className="text-slate-400 text-sm">Aucun produit disponible.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow p-6 border border-slate-100 flex flex-col h-80 overflow-hidden">
      <h3 className="text-lg font-semibold text-slate-800 mb-4">Top Produits</h3>
      <div className="flex-1 overflow-y-auto">
        <table className="min-w-full divide-y divide-slate-100">
          <thead>
            <tr className="bg-slate-50">
              <th
                scope="col"
                className="px-4 py-2.5 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider rounded-l-md"
              >
                Rang
              </th>
              <th
                scope="col"
                className="px-4 py-2.5 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider"
              >
                Produit / Catégorie
              </th>
              <th
                scope="col"
                className="px-4 py-2.5 text-right text-xs font-semibold text-slate-500 uppercase tracking-wider rounded-r-md"
              >
                Chiffre d'affaires
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 bg-white">
            {products.map((product, index) => {
              const rank = index + 1;
              const name =
                product.category ||
                (product.product_id
                  ? `Produit #${product.product_id.substring(0, 8)}`
                  : `Produit #${rank}`);
              const revenue = product.revenue || 0;

              return (
                <tr key={product.product_id || product.category || index} className="hover:bg-slate-50 transition-colors">
                  <td className="whitespace-nowrap px-4 py-3 text-sm font-medium text-slate-400">
                    #{rank}
                  </td>
                  <td
                    className="px-4 py-3 text-sm text-slate-800 font-medium truncate max-w-xs"
                    title={product.product_id || product.category}
                  >
                    {name}
                  </td>
                  <td className="whitespace-nowrap px-4 py-3 text-sm text-right text-slate-900 font-semibold">
                    {new Intl.NumberFormat("fr-FR", {
                      style: "currency",
                      currency: "EUR",
                    }).format(revenue)}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
