import { motion } from "framer-motion";

const products = [
  {
    name: "Black Oversized T-Shirt",
    sold: 148,
    growth: "+24%",
    width: "92%",
  },
  {
    name: "Premium Polo Shirt",
    sold: 121,
    growth: "+18%",
    width: "82%",
  },
  {
    name: "Women's Kurti",
    sold: 96,
    growth: "+13%",
    width: "70%",
  },
  {
    name: "Cargo Pants",
    sold: 84,
    growth: "+9%",
    width: "58%",
  },
];

function TopProducts() {
  return (
    <motion.div
      initial={{ opacity: 0, x: 40 }}
      animate={{ opacity: 1, x: 0 }}
      className="rounded-3xl border border-cyan-500/20 bg-slate-900/60 backdrop-blur-xl p-6"
    >
      <h2 className="text-2xl font-bold text-white mb-6">
        🔥 Top Selling Products
      </h2>

      <div className="space-y-6">
        {products.map((item) => (
          <div key={item.name}>
            <div className="flex justify-between mb-2">
              <div>
                <h3 className="text-white font-medium">
                  {item.name}
                </h3>

                <p className="text-slate-400 text-sm">
                  {item.sold} Units Sold
                </p>
              </div>

              <span className="text-green-400 font-semibold">
                {item.growth}
              </span>
            </div>

            <div className="w-full h-3 rounded-full bg-slate-800">
              <div
                style={{ width: item.width }}
                className="h-3 rounded-full bg-cyan-400"
              />
            </div>
          </div>
        ))}
      </div>
    </motion.div>
  );
}

export default TopProducts;