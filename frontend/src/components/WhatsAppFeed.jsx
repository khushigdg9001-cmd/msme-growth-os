import { motion } from "framer-motion";
import {
  MessageCircle,
  CheckCircle2,
  Truck,
  CreditCard,
} from "lucide-react";

const activities = [
  {
    icon: MessageCircle,
    title: "Fashion Hub Jaipur",
    message: "Requested 120 Black Oversized T-Shirts",
    time: "2 mins ago",
    color: "text-cyan-400",
  },
  {
    icon: Truck,
    title: "Metro Textile Mills",
    message: "Shipment dispatched • ETA 2 Days",
    time: "8 mins ago",
    color: "text-orange-400",
  },
  {
    icon: CreditCard,
    title: "Urban Trends Delhi",
    message: "Payment received • ₹48,200",
    time: "16 mins ago",
    color: "text-green-400",
  },
  {
    icon: CheckCircle2,
    title: "AI CEO",
    message: "Purchase order sent to supplier via WhatsApp",
    time: "21 mins ago",
    color: "text-purple-400",
  },
];

function WhatsAppFeed() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 40 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-3xl border border-cyan-500/20 bg-slate-900/60 backdrop-blur-xl p-6"
    >
      <h2 className="text-2xl font-bold text-white mb-6">
        💬 WhatsApp Business Activity
      </h2>

      <div className="space-y-4">
        {activities.map((item) => {
          const Icon = item.icon;

          return (
            <div
              key={item.title + item.time}
              className="rounded-2xl bg-slate-800/50 p-4 flex items-start gap-4"
            >
              <Icon
                size={24}
                className={item.color}
              />

              <div className="flex-1">
                <h3 className="text-white font-semibold">
                  {item.title}
                </h3>

                <p className="text-slate-400 text-sm mt-1">
                  {item.message}
                </p>

                <p className="text-slate-500 text-xs mt-2">
                  {item.time}
                </p>
              </div>
            </div>
          );
        })}
      </div>
    </motion.div>
  );
}

export default WhatsAppFeed;