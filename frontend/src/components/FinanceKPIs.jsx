import { IndianRupee, Wallet, TrendingUp, CreditCard } from "lucide-react";

function FinanceKPIs({ finance }) {

  const cards = [
    {
      title: "Revenue",
      value: `₹${finance.revenue.toLocaleString()}`,
      icon: IndianRupee,
      color: "text-cyan-400",
    },
    {
      title: "Expenses",
      value: `₹${finance.expenses.toLocaleString()}`,
      icon: CreditCard,
      color: "text-red-400",
    },
    {
      title: "Profit",
      value: `₹${finance.profit.toLocaleString()}`,
      icon: TrendingUp,
      color: "text-green-400",
    },
    {
      title: "Cash Balance",
      value: `₹${finance.cash.toLocaleString()}`,
      icon: Wallet,
      color: "text-yellow-400",
    },
  ];

  return (

    <div className="grid grid-cols-4 gap-6 mb-10">

      {cards.map((card) => {

        const Icon = card.icon;

        return (

          <div
            key={card.title}
            className="bg-slate-900 border border-cyan-500/20 rounded-2xl p-6"
          >

            <div className="flex justify-between items-center">

              <div>

                <p className="text-slate-400">
                  {card.title}
                </p>

                <h2 className={`text-3xl font-bold mt-2 ${card.color}`}>
                  {card.value}
                </h2>

              </div>

              <Icon
                className={card.color}
                size={34}
              />

            </div>

          </div>

        );

      })}

    </div>

  );

}

export default FinanceKPIs;