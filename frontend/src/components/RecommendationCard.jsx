import { motion } from "framer-motion";
import {
  Brain,
  CheckCircle2,
  MessageCircle,
  Pencil,
} from "lucide-react";

function RecommendationCard() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 40 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="rounded-3xl border border-cyan-500/20 bg-slate-900/60 backdrop-blur-xl p-8 shadow-2xl"
    >
      {/* Header */}

      <div className="flex items-center gap-3 mb-8">
        <Brain className="text-cyan-400" size={34} />

        <div>
          <h2 className="text-3xl font-bold text-white">
            AI CEO Command Center
          </h2>

          <p className="text-slate-400">
            Autonomous Business Decision Engine
          </p>
        </div>
      </div>

      {/* Executive Summary */}

      <div className="rounded-2xl bg-slate-800/50 p-6 mb-8">

        <h3 className="text-white font-semibold text-lg mb-4">
          📈 Today's Executive Summary
        </h3>

        <div className="grid grid-cols-2 gap-4">

          <div>
            <p className="text-slate-400 text-sm">
              Revenue Growth
            </p>

            <h2 className="text-green-400 text-2xl font-bold">
              +18%
            </h2>
          </div>

          <div>
            <p className="text-slate-400 text-sm">
              Business Risk
            </p>

            <h2 className="text-cyan-400 text-2xl font-bold">
              LOW
            </h2>
          </div>

          <div>
            <p className="text-slate-400 text-sm">
              AI Confidence
            </p>

            <h2 className="text-purple-400 text-2xl font-bold">
              96%
            </h2>
          </div>

          <div>
            <p className="text-slate-400 text-sm">
              Expected Profit
            </p>

            <h2 className="text-green-400 text-2xl font-bold">
              ₹64,800
            </h2>
          </div>

        </div>

      </div>

      {/* Decision Pipeline */}

      <div className="mb-8">

        <h3 className="text-white font-semibold mb-4">
          🤖 Multi-Agent Decision Pipeline
        </h3>

        <div className="space-y-3">

          {[
            "Inventory Agent analyzed stock levels",
            "Finance Agent verified cash flow",
            "Supplier Agent found 12% lower pricing",
            "CRM Agent predicted increased demand",
            "Compliance Agent verified GST impact",
          ].map((step) => (
            <div
              key={step}
              className="flex items-center gap-3 rounded-xl bg-slate-800/40 p-3"
            >
              <CheckCircle2
                className="text-green-400"
                size={20}
              />

              <span className="text-slate-300">
                {step}
              </span>
            </div>
          ))}

        </div>

      </div>

      {/* Final Decision */}

      <div className="rounded-2xl border border-cyan-500/20 bg-cyan-500/10 p-6">

        <h3 className="text-white font-semibold text-lg mb-3">
          🎯 Final AI Decision
        </h3>

        <h2 className="text-cyan-400 text-2xl font-bold">
          Increase Black Oversized T-Shirt Inventory
        </h2>

        <div className="grid grid-cols-3 gap-6 mt-6">

          <div>
            <p className="text-slate-400 text-sm">
              Current Stock
            </p>

            <h3 className="text-red-400 text-xl font-bold">
              18 Units
            </h3>
          </div>

          <div>
            <p className="text-slate-400 text-sm">
              Recommended Order
            </p>

            <h3 className="text-green-400 text-xl font-bold">
              150 Units
            </h3>
          </div>

          <div>
            <p className="text-slate-400 text-sm">
              Supplier
            </p>

            <h3 className="text-cyan-400 text-xl font-bold">
              Metro Textile Mills
            </h3>
          </div>

        </div>

        <div className="flex gap-4 mt-8">

          <button className="flex items-center gap-2 rounded-xl bg-cyan-500 hover:bg-cyan-400 px-6 py-3 text-black font-semibold transition">

            <CheckCircle2 size={20} />

            Approve

          </button>

          <button className="flex items-center gap-2 rounded-xl border border-yellow-500 px-6 py-3 text-yellow-400 hover:bg-yellow-500 hover:text-black transition">

            <Pencil size={18} />

            Modify

          </button>

          <button className="flex items-center gap-2 rounded-xl border border-green-500 px-6 py-3 text-green-400 hover:bg-green-500 hover:text-black transition">

            <MessageCircle size={18} />

            Send to WhatsApp

          </button>

        </div>

      </div>

    </motion.div>
  );
}

export default RecommendationCard;