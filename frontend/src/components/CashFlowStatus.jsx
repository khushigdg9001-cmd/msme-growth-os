import { CircleCheckBig, CircleAlert } from "lucide-react";

function CashFlowStatus({ finance }) {

  const healthy = finance.cash > finance.expenses;

  return (
    <div className="bg-slate-900 rounded-2xl border border-cyan-500/20 p-8">

      <h2 className="text-2xl font-bold text-cyan-400">
        Cash Flow Status
      </h2>

      <p className="text-slate-400 mt-2">
        Live liquidity monitoring
      </p>

      <div className="mt-8 flex items-center gap-4">

        {healthy ? (
          <CircleCheckBig
            size={48}
            className="text-green-400"
          />
        ) : (
          <CircleAlert
            size={48}
            className="text-red-400"
          />
        )}

        <div>

          <h3
            className={`text-3xl font-bold ${
              healthy
                ? "text-green-400"
                : "text-red-400"
            }`}
          >
            {healthy
              ? "Healthy Cash Flow"
              : "Low Cash Flow"}
          </h3>

          <p className="text-slate-400 mt-2">
            Cash Available :
            ₹{finance.cash.toLocaleString()}
          </p>

        </div>

      </div>

    </div>
  );
}

export default CashFlowStatus;