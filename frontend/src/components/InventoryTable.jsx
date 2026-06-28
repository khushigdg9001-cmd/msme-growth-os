function InventoryTable({ products = [] }) {
  return (
    <div className="mt-8 bg-slate-900 rounded-2xl border border-cyan-500/20 overflow-hidden">

      <table className="w-full">

        <thead className="bg-slate-800 text-cyan-300">
          <tr>
            <th className="p-4 text-left">Product</th>
            <th className="text-center">Stock</th>
            <th className="text-center">Forecast</th>
            <th className="text-center">Supplier</th>
            <th className="text-center">Status</th>
          </tr>
        </thead>

        <tbody>

          {products.length === 0 ? (

            <tr>
              <td
                colSpan="5"
                className="p-8 text-center text-slate-400"
              >
                No Products Found
              </td>
            </tr>

          ) : (

            products.map((p) => (

              <tr
                key={p.id}
                className="border-t border-slate-700 hover:bg-cyan-500/10 transition-all duration-300"
              >

                <td className="p-4 font-semibold text-white">
                  {p.product}
                </td>

                <td className="text-center text-slate-300">
                  {p.stock}
                </td>

                <td className="text-center text-slate-300">
                  {p.forecast}
                </td>

                <td className="text-center text-slate-300">
                  {p.supplier}
                </td>

                <td className="text-center">

                  <span
                    className={`px-3 py-1 rounded-full text-sm font-semibold ${
                      p.status === "Healthy"
                        ? "bg-green-500/20 text-green-400"
                        : p.status === "Restock"
                        ? "bg-yellow-500/20 text-yellow-400"
                        : "bg-red-500/20 text-red-400"
                    }`}
                  >
                    {p.status}
                  </span>

                </td>

              </tr>

            ))

          )}

        </tbody>

      </table>

    </div>
  );
}

export default InventoryTable;