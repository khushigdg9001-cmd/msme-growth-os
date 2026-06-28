import { useEffect, useState } from "react";
import { getAICEO } from "../api/aiceo";

import Sidebar from "../components/Sidebar";
import AgentTimeline from "../components/AgentTimeline";

function AICEO() {

  const [data, setData] = useState(null);

  useEffect(() => {

    async function loadCEO() {

      try {

        const result = await getAICEO();

        setData(result);

      } catch (err) {

        console.error(err);

      }

    }

    loadCEO();

  }, []);

  if (!data) {

    return (

      <div className="min-h-screen bg-slate-950 flex justify-center items-center text-cyan-400 text-4xl font-bold">

        Loading AI CEO...

      </div>

    );

  }

  return (

    <div className="flex min-h-screen bg-slate-950">

      <Sidebar />

      <main className="flex-1 overflow-y-auto p-10">

        <div className="flex justify-between items-center mb-10">

          <div>

            <h1 className="text-5xl font-black text-cyan-400">

              AI CEO Command Center

            </h1>

            <p className="text-slate-400 mt-3">

              Autonomous business strategy generated from all AI agents.

            </p>

          </div>

          <div className="text-right">

            <div className="flex items-center gap-2 justify-end">

              <div className="w-3 h-3 rounded-full bg-green-400 animate-pulse"></div>

              <span className="text-green-400 font-semibold">

                LIVE

              </span>

            </div>

            <p className="text-slate-500 mt-2">

              AI CEO Active

            </p>

          </div>

        </div>

        <div className="grid grid-cols-4 gap-6 mb-8">

          <div className="bg-slate-900 rounded-2xl p-6 border border-cyan-500/20">

            <p className="text-slate-400">

              Business Health

            </p>

            <h2 className="text-5xl font-black text-cyan-400 mt-3">

              {data.businessHealth}%

            </h2>

          </div>

          <div className="bg-slate-900 rounded-2xl p-6 border border-cyan-500/20">

            <p className="text-slate-400">

              Growth Score

            </p>

            <h2 className="text-5xl font-black text-green-400 mt-3">

              {data.growthScore}

            </h2>

          </div>

          <div className="bg-slate-900 rounded-2xl p-6 border border-cyan-500/20">

            <p className="text-slate-400">

              Expected Profit

            </p>

           <h2 className="text-3xl lg:text-4xl font-black text-yellow-400 mt-3 whitespace-nowrap">
  ₹{data.expectedProfit.toLocaleString()}
</h2>
          </div>

          <div className="bg-slate-900 rounded-2xl p-6 border border-cyan-500/20">

            <p className="text-slate-400">

              AI Decisions

            </p>

            <h2 className="text-5xl font-black text-purple-400 mt-3">

              {data.decisions.length}

            </h2>

          </div>

        </div>              {/* Agent Status */}

        <div className="grid grid-cols-4 gap-6 mb-8">

          <div className="bg-slate-900 rounded-2xl p-6 border border-cyan-500/20">
            <p className="text-slate-400">Inventory</p>
            <h3 className="text-2xl font-bold text-cyan-400 mt-2">
              {data.inventoryStatus}
            </h3>
          </div>

          <div className="bg-slate-900 rounded-2xl p-6 border border-cyan-500/20">
            <p className="text-slate-400">Finance</p>
            <h3 className="text-2xl font-bold text-green-400 mt-2">
              {data.financeStatus}
            </h3>
          </div>

          <div className="bg-slate-900 rounded-2xl p-6 border border-cyan-500/20">
            <p className="text-slate-400">CRM</p>
            <h3 className="text-2xl font-bold text-yellow-400 mt-2">
              {data.crmStatus}
            </h3>
          </div>

          <div className="bg-slate-900 rounded-2xl p-6 border border-cyan-500/20">
            <p className="text-slate-400">Compliance</p>
            <h3 className="text-2xl font-bold text-purple-400 mt-2">
              {data.complianceStatus}
            </h3>
          </div>

        </div>

        {/* AI CEO Decisions */}
<AgentTimeline />
        <div className="bg-slate-900 rounded-2xl border border-cyan-500/20 overflow-hidden mb-8">

          <div className="p-6 border-b border-slate-700">

            <h2 className="text-3xl font-bold text-white">
              AI Executive Decisions
            </h2>

            <p className="text-slate-400 mt-2">
              Live strategic recommendations generated from all business agents.
            </p>

          </div>

          <table className="w-full">

            <thead className="bg-slate-800">

              <tr>

                <th className="text-left p-5 text-cyan-300">Agent</th>

                <th className="text-left p-5 text-cyan-300">Priority</th>

                <th className="text-left p-5 text-cyan-300">Decision</th>

                <th className="text-left p-5 text-cyan-300">Confidence</th>

              </tr>

            </thead>

            <tbody>

              {data.decisions.map((decision, index) => (

                <tr
                  key={index}
                  className="border-t border-slate-700 hover:bg-slate-800/40"
                >

                  <td className="p-5 text-white">
                    {decision.agent}
                  </td>

                  <td className="p-5">

                    <span
                      className={`px-4 py-2 rounded-full text-sm font-semibold ${
                        decision.priority === "High"
                          ? "bg-red-500/20 text-red-400"
                          : "bg-yellow-500/20 text-yellow-400"
                      }`}
                    >
                      {decision.priority}
                    </span>

                  </td>

                  <td className="p-5">

                    <h3 className="text-white font-semibold">
                      {decision.title}
                    </h3>

                    <p className="text-slate-400 mt-1">
                      {decision.reason}
                    </p>

                  </td>

                  <td className="p-5 text-green-400 font-bold">
                    {decision.confidence}
                  </td>

                </tr>

              ))}

            </tbody>

          </table>

        </div>

        {/* Executive Summary */}

        <div className="bg-gradient-to-r from-cyan-500/10 to-blue-500/10 border border-cyan-500/30 rounded-2xl p-8">

          <h2 className="text-3xl font-bold text-cyan-300 mb-4">
            AI CEO Executive Summary
          </h2>

          <p className="text-slate-300 leading-8 text-lg">

            The AI CEO continuously evaluates inventory, finance, CRM and
            compliance data to identify operational risks and growth
            opportunities. Current business health is
            <span className="text-cyan-400 font-bold">
              {" "} {data.businessHealth}%{" "}
            </span>
            with an expected profit of
            <span className="text-green-400 font-bold">
              {" "}₹{data.expectedProfit.toLocaleString()}{" "}
            </span>
            next cycle. Strategic actions shown above are prioritized
            automatically based on live agent outputs.

          </p>

        </div>

      </main>

    </div>

  );

}

export default AICEO;