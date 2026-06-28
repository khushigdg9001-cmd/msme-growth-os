import {
  Boxes,
  PackageCheck,
  Activity,
  TrendingUp,
} from "lucide-react";

function InventoryKPIs() {

  const cards = [

    {
      title: "Inventory Value",
      value: "₹1.82 L",
      icon: Boxes,
      color: "text-cyan-400",
    },

    {
      title: "Products",
      value: "126",
      icon: PackageCheck,
      color: "text-green-400",
    },

    {
      title: "AI Health Score",
      value: "94%",
      icon: Activity,
      color: "text-purple-400",
    },

    {
      title: "Forecast Accuracy",
      value: "92%",
      icon: TrendingUp,
      color: "text-orange-400",
    },

  ];

  return (

    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-7 mb-10">

      {cards.map((card) => {

        const Icon = card.icon;

        return (

          <div
            key={card.title}
            className="bg-slate-900 border border-cyan-500/20 rounded-3xl p-8 hover:border-cyan-400 transition-all duration-300"
          >

            <div className="flex justify-between items-start">

              <div>

                <p className="text-slate-400 text-sm">
                  {card.title}
                </p>

                <h2 className={`text-5xl font-black mt-5 ${card.color}`}>
                  {card.value}
                </h2>

              </div>

              <Icon
                size={42}
                className={card.color}
              />

            </div>

          </div>

        );

      })}

    </div>

  );

}

export default InventoryKPIs;