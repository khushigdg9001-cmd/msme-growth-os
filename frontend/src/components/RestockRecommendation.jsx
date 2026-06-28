import { Brain } from "lucide-react";

function RestockRecommendation() {
  return (
    <div className="mt-8 rounded-2xl bg-slate-900 border border-cyan-500/20 p-6">

      <div className="flex items-center gap-3">

        <Brain className="text-cyan-400" />

        <h2 className="text-2xl font-bold text-white">
          AI Restock Recommendation
        </h2>

      </div>

      <div className="mt-6 space-y-4">

        <div className="bg-slate-800 rounded-xl p-5">

          <h3 className="text-cyan-400 text-xl font-semibold">
            Restock High-Demand Products Immediately
          </h3>

          <p className="text-slate-300 mt-2">
            Black Oversized Tee (18→147 forecast),
White Hoodie (12→86 forecast)
and Premium Polo Shirt (8→115 forecast)
are expected to go out of stock within days.

AI recommends placing an immediate purchase order to Metro Textile, Classic Cotton and Elite Fashion.
          </p>

        </div>

      </div>

    </div>
  );
}

export default RestockRecommendation;