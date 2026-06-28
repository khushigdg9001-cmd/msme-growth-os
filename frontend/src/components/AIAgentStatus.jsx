import { motion } from "framer-motion";
import {
  Brain,
  Boxes,
  Wallet,
  Users,
  Truck,
  ShieldCheck,
} from "lucide-react";

const agents = [
  {
    icon: Boxes,
    name: "Inventory Agent",
    status: "Monitoring Stock Levels",
  },
  {
    icon: Wallet,
    name: "Finance Agent",
    status: "Forecasting Cash Flow",
  },
  {
    icon: Users,
    name: "CRM Agent",
    status: "Analyzing Customer Activity",
  },
  {
    icon: Truck,
    name: "Supplier Agent",
    status: "Comparing Supplier Prices",
  },
  {
    icon: ShieldCheck,
    name: "Compliance Agent",
    status: "Checking GST Compliance",
  },
  {
    icon: Brain,
    name: "AI CEO",
    status: "Generating Business Decisions",
  },
];

function AIAgentStatus() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 40 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-3xl border border-cyan-500/20 bg-slate-900/60 backdrop-blur-xl p-6"
    >
      <h2 className="text-2xl font-bold text-white mb-6">
        🤖 AI Agents
      </h2>

      <div className="space-y-4">
        {agents.map((agent) => {
          const Icon = agent.icon;

          return (
            <div
              key={agent.name}
              className="flex items-center justify-between rounded-2xl bg-slate-800/60 p-4"
            >
              <div className="flex items-center gap-4">
                <Icon
                  className="text-cyan-400"
                  size={24}
                />

                <div>
                  <h3 className="text-white font-semibold">
                    {agent.name}
                  </h3>

                  <p className="text-slate-400 text-sm">
                    {agent.status}
                  </p>
                </div>
              </div>

              <div className="flex items-center gap-2">
                <span className="w-3 h-3 rounded-full bg-green-400 animate-pulse"></span>

                <span className="text-green-400">
                  Active
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </motion.div>
  );
}

export default AIAgentStatus;