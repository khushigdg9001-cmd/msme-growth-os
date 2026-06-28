function ComplianceTable({ documents }) {

  return (

    <div className="mt-8 bg-slate-900 rounded-2xl border border-cyan-500/20 overflow-hidden">

      <div className="p-6">

        <h2 className="text-3xl font-bold text-white">

          Compliance Overview

        </h2>

        <p className="text-slate-400 mt-2">

          Live legal documents monitored by Compliance Agent

        </p>

      </div>

      <table className="w-full">

        <thead className="bg-slate-800 text-cyan-300">

          <tr>

            <th className="text-left p-5">

              Document

            </th>

            <th>

              Status

            </th>

            <th>

              Due Date

            </th>

          </tr>

        </thead>

        <tbody>

          {documents.map((doc, index) => (

            <tr
              key={index}
              className="border-t border-slate-700 hover:bg-slate-800/40"
            >

              <td className="p-5 text-white">

                {doc.document}

              </td>

              <td>

                <span
                  className={`px-3 py-1 rounded-full text-sm font-semibold

                  ${
                    doc.status === "Filed" || doc.status === "Valid"

                      ? "bg-green-500/20 text-green-400"

                      : doc.status === "Expiring"

                      ? "bg-yellow-500/20 text-yellow-400"

                      : "bg-red-500/20 text-red-400"

                  }

                  `}
                >

                  {doc.status}

                </span>

              </td>

              <td className="text-slate-300">

                {doc.dueDate}

              </td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>

  );

}

export default ComplianceTable;