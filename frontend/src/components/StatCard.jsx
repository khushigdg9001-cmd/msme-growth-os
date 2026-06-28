import { motion } from "framer-motion";

function StatCard({
  title,
  value,
  change,
  color = "text-cyan-400",
}) {
  return (
    <motion.div
      whileHover={{ scale: 1.04 }}
      className="rounded-3xl border border-cyan-500/20 bg-slate-900/60 backdrop-blur-xl p-6 shadow-xl"
    >
      <p className="text-slate-400 text-sm">
        {title}
      </p>

      <h2 className={`text-4xl font-bold mt-3 ${color}`}>
        {value}
      </h2>

      <p className="text-green-400 mt-4">
        {change}
      </p>
    </motion.div>
  );
}

export default StatCard;