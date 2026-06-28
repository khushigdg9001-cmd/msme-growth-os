import { useEffect, useState } from "react";

import Sidebar from "../components/Sidebar";
import FinanceKPIs from "../components/FinanceKPIs";
import RevenueChart from "../components/RevenueChart";
import FinancialReport from "../components/FinancialReport";
import PendingPayments from "../components/PendingPayments";
import CashFlowStatus from "../components/CashFlowStatus";
import FinanceRecommendation from "../components/FinanceRecommendation";

import { getFinance } from "../api/finance";

function Finance() {
  const [finance, setFinance] = useState(null);

  useEffect(() => {
    async function loadFinance() {
      try {
        const data = await getFinance();

        console.log("Finance API:", data);

        setFinance(data);
      } catch (error) {
        console.error(error);
      }
    }

    loadFinance();
  }, []);

  if (!finance) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <h1 className="text-cyan-400 text-3xl font-bold">
          Loading Finance Agent...
        </h1>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-slate-950">

      <Sidebar />

      <main className="flex-1 overflow-y-auto p-10">

        {/* Header */}

        <div className="flex items-center justify-between mb-10">

          <div>

            <h1 className="text-5xl font-black text-cyan-400">
              Finance Intelligence
            </h1>

            <p className="text-slate-400 mt-3">
              AI powered financial monitoring, cash flow analysis and
              autonomous decision making.
            </p>

          </div>

          <div className="text-right">

            <div className="flex items-center justify-end gap-2">

              <div className="h-3 w-3 rounded-full bg-green-400 animate-pulse"></div>

              <span className="text-green-400 font-semibold">
                LIVE
              </span>

            </div>

            <p className="text-slate-500 mt-2">
              Finance Agent Active
            </p>

          </div>

        </div>

        {/* KPIs */}

        <FinanceKPIs finance={finance} />

        {/* Revenue Chart */}

        <RevenueChart finance={finance} />

        {/* Financial Report */}

        <FinancialReport finance={finance} />

        {/* Pending + Cash Flow */}

        <div className="grid grid-cols-2 gap-6 mt-8">

          <PendingPayments finance={finance} />

          <CashFlowStatus finance={finance} />

        </div>

        {/* AI Recommendation */}

        <FinanceRecommendation
          recommendation={finance.recommendation}
        />

      </main>

    </div>
  );
}

export default Finance;