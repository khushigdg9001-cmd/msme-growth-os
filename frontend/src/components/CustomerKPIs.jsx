import {
  Users,
  UserCheck,
  UserPlus,
  TrendingUp,
} from "lucide-react";

function CustomerKPIs({ crm }) {

  const cards = [

    {
      title: "Customers",
      value: crm.customers,
      icon: Users,
      color: "text-cyan-400",
    },

    {
      title: "Active Customers",
      value: crm.activeCustomers,
      icon: UserCheck,
      color: "text-green-400",
    },

    {
      title: "New Leads",
      value: crm.newLeads,
      icon: UserPlus,
      color: "text-orange-400",
    },

    {
      title: "Conversion Rate",
      value: `${crm.conversionRate}%`,
      icon: TrendingUp,
      color: "text-purple-400",
    },

  ];

  return (

    <div className="grid grid-cols-4 gap-6">

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
                size={32}
                className={card.color}
              />

            </div>

          </div>

        );

      })}

    </div>

  );

}

export default CustomerKPIs;