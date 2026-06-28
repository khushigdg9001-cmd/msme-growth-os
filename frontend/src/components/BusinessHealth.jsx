import { motion } from "framer-motion";
import {
  Activity,
  TrendingUp,
  Package,
  Users,
  Wallet,
} from "lucide-react";

function BusinessHealth() {
  return (
    <motion.div
      initial={{ opacity: 0, x: 30 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.6 }}
      className="rounded-3xl border border-cyan-500/20 bg-slate-900/60 backdrop-blur-xl p-8 shadow-2xl"
    >
      <div className="flex items-center gap-3 mb-6">
        <Activity className="text-cyan-400" size={30} />
        <h2 className="text-2xl font-bold text-white">
          Business Health
        </h2>
      </div>

      <div className="flex items-center justify-center my-8">
        <div className="w-40 h-40 rounded-full border-[10px] border-cyan-400 flex items-center justify-center">
          <div className="text-center">
            <h1 className="text-5xl font-bold text-cyan-400">
              91%
            </h1>

            <p className="text-slate-400 text-sm mt-2">
              Excellent
            </p>
          </div>
        </div>
      </div>

      <div className="space-y-5">

        <div className="flex justify-between">
          <div className="flex gap-2 items-center">
            <TrendingUp className="text-green-400" size={18}/>
            <span className="text-slate-300">
              Revenue Growth
            </span>
          </div>

          <span className="text-green-400 font-semibold">
            +18%
          </span>
        </div>

        <div className="flex justify-between">
          <div className="flex gap-2 items-center">
            <Package className="text-orange-400" size={18}/>
            <span className="text-slate-300">
              Inventory Status
            </span>
          </div>

          <span className="text-orange-400 font-semibold">
            Good
          </span>
        </div>

        <div className="flex justify-between">
          <div className="flex gap-2 items-center">
            <Users className="text-cyan-400" size={18}/>
            <span className="text-slate-300">
              Customer Retention
            </span>
          </div>

          <span className="text-cyan-400 font-semibold">
            94%
          </span>
        </div>

        <div className="flex justify-between">
          <div className="flex gap-2 items-center">
            <Wallet className="text-green-400" size={18}/>
            <span className="text-slate-300">
              Cash Flow
            </span>
          </div>

          <span className="text-green-400 font-semibold">
            Healthy
          </span>
        </div>

      </div>
    </motion.div>
  );
}

export default BusinessHealth;