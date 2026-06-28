function CustomerTable({ customers }) {

  return (

    <div className="mt-8 bg-slate-900 rounded-2xl border border-cyan-500/20 overflow-hidden">
<div className="p-6">

  <h2 className="text-3xl font-bold text-white">

    Customer Intelligence

  </h2>

  <p className="text-slate-400 mt-2">

    Recent high-value customer interactions

  </p>

</div>
      <table className="w-full">

        <thead className="bg-slate-800 text-cyan-300">

          <tr>

            <th className="p-4 text-left">Customer</th>

            <th>Company</th>

            <th>Last Purchase</th>

            <th>Value</th>

            <th>Status</th>

          </tr>

        </thead>

        <tbody>

          {customers.map((customer) => (

            <tr

              key={customer.id}

              className="border-t border-slate-700 hover:bg-cyan-500/10 transition-all duration-300"

            >

              <td className="p-4 font-semibold text-white">

                {customer.name}

              </td>

              <td className="text-slate-300">

                {customer.company}

              </td>

              <td className="text-slate-300">

                {customer.lastPurchase}

              </td>

              <td className="text-green-400 font-semibold">

                {customer.value}

              </td>

              <td>

                <span

                  className={`px-3 py-1 rounded-full text-sm font-semibold

                  ${

                    customer.status === "Active"

                      ? "bg-green-500/20 text-green-400"

                      : customer.status === "Inactive"

                      ? "bg-red-500/20 text-red-400"

                      : "bg-yellow-500/20 text-yellow-400"

                  }

                  `}

                >

                  {customer.status}

                </span>

              </td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>

  );

}

export default CustomerTable;