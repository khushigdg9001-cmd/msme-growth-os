import { motion } from "framer-motion";
import { TriangleAlert } from "lucide-react";

const alerts = [
  {
    product: "Black Oversized T-Shirt",
    stock: 18,
    minimum: 60,
  },
  {
    product: "Women's Kurti",
    stock: 12,
    minimum: 40,
  },
  {
    product: "Cargo Pants",
    stock: 25,
    minimum: 50,
  },
];

function InventoryAlerts() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 40 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-3xl border border-red-500/20 bg-slate-900/60 backdrop-blur-xl p-6"
    >
      <div className="flex items-center gap-3 mb-6">
        <TriangleAlert className="text-red-400" />
        <h2 className="text-2xl font-bold text-white">
          Inventory Alerts
        </h2>
      </div>

      <div className="space-y-5">
        {alerts.map((item) => (
          <div
            key={item.product}
            className="rounded-xl bg-slate-800/60 p-4"
          >
            <h3 className="text-white font-semibold">
              {item.product}
            </h3>

            <p className="text-red-400 mt-2">
              Current Stock : {item.stock}
            </p>

            <p className="text-slate-400 text-sm">
              Minimum Required : {item.minimum}
            </p>

            <button className="mt-4 rounded-lg bg-red-500 px-4 py-2 text-white hover:bg-red-400 transition">
              Restock Now
            </button>
          </div>
        ))}
      </div>
    </motion.div>
  );
}

export default InventoryAlerts;